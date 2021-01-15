from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from cssutils import CSSParser, CSSSerializer
import requests
from bs4 import BeautifulSoup
from flask import Flask, Response, request

app = Flask(__name__, static_folder=None, template_folder=None)

defaultDomain = "https://en.wikipedia.org"
linkAttr = ["href", "src"]


# ? Remove original URLs and add targetDomain QueryString
def clearLink(link):
    url = urlparse(link)

    qs = parse_qs(url.query)
    if url.netloc != "":
        qs["targetDomain"] = url.netloc
    else:
        qs["targetDomain"] = defaultDomain

    url = url._replace(netloc="", scheme="", query=urlencode(qs))

    return urlunparse(url)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    if request.args.get("targetDomain") != None:
        # ? Remove targetDomain from QueryString
        url = urlparse(request.full_path)

        qs = parse_qs(url.query)
        qs.pop("targetDomain", None)
        url._replace(query=urlencode(qs))

        # ? GET
        try:
            r = requests.get(request.scheme + "://" + request.args.get(
                "targetDomain").replace("http://", "").replace("https://", "") + urlunparse(url))
            print(r.status_code)
            # print(f"REQUEST -> ", bytes(request.scheme + "://" + request.args.get(
            # "targetDomain") + urlunparse(url), "utf8"))
        except Exception as err:
            print("ERROR -> " + str(err))
            return str(err)

        doc = r.content

        # ? Modify all href and src attrs
        if "text/html" in r.headers['content-type']:
            soup = BeautifulSoup(doc, 'html.parser')
            for attr in linkAttr:
                for tag in soup.findAll(**{attr: True}):
                    tag[attr] = clearLink(tag[attr])
            doc = str(soup)

        return Response(doc, mimetype=r.headers['content-type'])
    else:
        print("->", request.full_path)
        return "No specified target domain!"

if __name__ == "__main__":
    app.run()
