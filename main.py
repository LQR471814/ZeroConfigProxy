import logging
import re
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup
from flask import Flask, Response, request, abort

app = Flask(__name__, static_folder=None, template_folder=None)

HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT',
                'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

defaultDomain = "facebook.com"
linkAttr = {"href": {"href": True},
            "src": {"src": True},
            "action": {"action": True},
            "data": {"data": True},
            "profile": {"profile": True},
            "cite": {"cite": True},
            "classid": {"classid": True},
            "codebase": {"codebase": True},
            "data": {"data": True},
            "usemap": {"usemap": True},
            "formaction": {"formaction": True},
            "icon": {"icon": True},
            "manifest": {"manifest": True},
            "poster": {"poster": True},
            "content": {"content": True,  # ? To catch the Open Graph Protocol and some twitter metadata exhibited in <meta> tags, see https://ogp.me/
                        "property": lambda inp:
                            inp == "og:url" or
                            inp == "og:image" or
                            inp == "og:audio" or
                            inp == "og:video" or
                            inp == "og:image:secure_url" or
                            inp == "twitter:image"
                        }}

# * There are some that I have missed but I don't want to
# * implement those the likes of which aren't used commonly either

# ? Remove original URLs and add targetDomain QueryString

corsHandlerScript = open("utils/cors_handler.js", "r").read()

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

session = requests.Session()


def clearLink(link):
    url = urlparse(link)

    qs = parse_qs(url.query)
    if url.netloc != "":
        qs["targetDomain"] = url.netloc

    url = url._replace(netloc="", scheme="", query=urlencode(qs))

    return urlunparse(url)


def cssRegex(match):
    return f"url({clearLink(match.group(1))})"


@app.route('/', defaults={'path': ''}, methods=HTTP_METHODS)
@app.route('/<path:path>')
def home(path):
    if request.args.get("targetDomain") == None:
        domain = defaultDomain
    else:
        domain = request.args.get("targetDomain")

    # ? Remove targetDomain from QueryString
    url = urlparse(request.full_path.replace(
        "%5B", "").replace("%5D", "").replace("%27", ""))

    qs = parse_qs(url.query)
    qs.pop("targetDomain", None)
    url = url._replace(query=urlencode(qs))

    reqUrl = request.scheme + "://" + domain.replace(
        "http://", "").replace("https://", "") + urlunparse(url).replace("%5B", "").replace("%5D", "").replace("%27", "")

    if request.method == "GET":  # ? GET Requests
        try:
            r = session.get(reqUrl)
        except Exception as err:
            print("ERROR -> " + str(err))
            return str(err)

        doc = r.content
        requestMimeType = r.headers.get('content-type', '')

        # ? Modify all href and src attrs
        if "text/html" in requestMimeType:
            soup = BeautifulSoup(doc, 'html.parser')

            # ? Injecting CORS Handler for JS XMLHttpRequests
            if soup.head == None:
                soup.insert(0, soup.new_tag("head"))
            corsHandler = soup.new_tag("script")
            corsHandler.string = corsHandlerScript
            soup.head.insert(0, corsHandler)

            for attr in linkAttr:
                for tag in soup.findAll(**linkAttr[attr]):
                    tag[attr] = clearLink(tag[attr])
            for style in soup.findAll("style"):
                if style.string == None:
                    style.string = ""
                style.string = re.sub(r'url\((.*?)\)', cssRegex, style.string)
            doc = str(soup)
        elif "text/css" in requestMimeType:
            css = re.sub(r'url\((.*?)\)', cssRegex, doc.decode("utf8"))
            doc = css.encode("utf8")
    elif request.method == "POST":  # ? POST Requests
        r = requests.post(reqUrl, data=request.form)
        requestMimeType = r.headers.get('content-type', '')
        doc = r.content
    else:  # ? Unsupported method
        print("UNSUPPORTED:", request.method)
        abort(405)
    return Response(doc, mimetype=requestMimeType)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
