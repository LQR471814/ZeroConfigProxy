from urllib.parse import urlparse

from flask import Flask, request

from common.html_definitions import *
from common.types import *
from process.request import *
from utils.parsing_utils import *

homepage = open("index.html", "r").read()
homepage = homepage.replace("\"INSERT_NORMALIZE_URL\"", normalizeUrlScript)

app = Flask(__name__, static_folder=None, template_folder=None)

#? When user initializes request
@app.route('/')
def home():
    return homepage

#? When other requests come in
@app.route('/Request', methods=HTTP_METHODS)
def request_route():
    requestURL = urlparse(request.url)
    own_host = requestURL.netloc #? Get own server host

    target_url = get_target_url(requestURL)
    if not target_url:
        return 'You forgot a target url'

    context = RequestContext(
        own_host=own_host,
        target_url=target_url
    )

    print(f'\n\tRequest\n\ttarget_url: {target_url}\n')

    if request.method == 'GET':
        response = process_get(context)

    #? Set cookie to be sent on every client request thereafter
    response.set_cookie('targetDomain', context.target_parsed.netloc)

    return response

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    domain = request.cookies.get('targetDomain', None)
    if not domain:
        return "Origin wasn't in cookies bro"

    if request.method == "GET":
        data = requests.get(f'{request.scheme}://{domain}/{path}')
        response = make_typed_response(
            data.content,
            data.headers.get('content-type', '')
        )

        return response
    else:
        return "Method not supported!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
