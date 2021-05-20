import logging
from urllib.parse import urlparse

from flask import Flask, request

from common.html_definitions import *
from common.types import *
from process.request import *
from utils.parsing_utils import *

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__, static_folder=None, template_folder=None)

#? When user initializes request
@app.route('/')
def home():
    return 'Use path /Request with ?targetUrl for now'

#? When other requests come in
@app.route('/Request', methods=HTTP_METHODS)
def request_route():
    requestURL = urlparse(request.url)
    own_host = requestURL.netloc #? Get own server host

    target_url = get_target_url(requestURL)
    if not target_url:
        return 'You forgot a target url'

    print(f'\n\tRequest\n\ttarget_url: {target_url}\n')

    if request.method == 'GET':
        return process_get(RequestContext(
           own_host=own_host,
           target_url=target_url
        ))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
