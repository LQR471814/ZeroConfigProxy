import logging
import re
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup
from flask import Flask, Response, request

app = Flask(__name__, static_folder=None, template_folder=None)

defaultDomain = "en.wikipedia.com"
linkAttr = ["href",
            "src",
            "action",
            "data",
            "profile",
            "cite",
            "classid",
            "codebase",
            "data",
            "usemap",
            "formaction",
            "icon",
            "manifest",
            "poster"]

# * There are some that I have missed but I don't want to
# * implement those the likes of which aren't used commonly either

# ? Remove original URLs and add targetDomain QueryString


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


def clearLink(link):
    url = urlparse(link)

    qs = parse_qs(url.query)
    if url.netloc != "":
        qs["targetDomain"] = url.netloc

    url = url._replace(netloc="", scheme="", query=urlencode(qs))

    return urlunparse(url)


def cssRegex(match):
    return f"url({clearLink(match.group(1))})"


@app.route('/', defaults={'path': ''})
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

    # ? GET
    try:
        reqUrl = request.scheme + "://" + domain.replace(
            "http://", "").replace("https://", "") + urlunparse(url).replace("%5B", "").replace("%5D", "").replace("%27", "")
        r = requests.get(reqUrl)

    except Exception as err:
        print("ERROR -> " + str(err))
        return str(err)

    doc = r.content

    # ? Modify all href and src attrs
    if "text/html" in r.headers.get('content-type', ''):
        soup = BeautifulSoup(doc, 'html.parser')
        for attr in linkAttr:
            for tag in soup.findAll(**{attr: True}):
                tag[attr] = clearLink(tag[attr])
        for style in soup.findAll("style"):
            style.string = re.sub(r'url\((.*?)\)', cssRegex, style.string)
        doc = str(soup)
    elif "text/css" in r.headers.get('content-type', ''):
        css = re.sub(r'url\((.*?)\)', cssRegex, doc.decode("utf8"))
        doc = css.encode("utf8")

    return Response(doc, mimetype=r.headers.get('content-type', ''))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)
