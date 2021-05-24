import requests
from common.html_definitions import *
from common.types import *
from flask import make_response
from utils.parsing_utils import *

from process.content import *

session = requests.Session()

def make_typed_response(content, mimetype):
    response = make_response(content)
    response.headers['content-type'] = mimetype
    return response

def process_get(req_context: RequestContext) -> str:
    try:
        data = requests.get(req_context.target_url)
    except:
        return f"Server failed to request {req_context.target_url}. Is this a valid URL?"

    data_mimetype = data.headers.get('content-type', '')

    if 'text/html' in data_mimetype:
        return make_typed_response(
            process_html(data.content, req_context),
            data_mimetype
        )
    elif 'text/css' in data_mimetype:
        return make_typed_response(
            process_css(data.text, req_context),
            data_mimetype
        )
    else:
        return make_typed_response(
            data.content,
            data_mimetype
        )
