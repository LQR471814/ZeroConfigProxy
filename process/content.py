import re

from bs4 import BeautifulSoup
from common.html_definitions import *
from common.types import *
from utils.parsing_utils import *

jsRequestHandler = open('request_handler.js', 'r').read()
normalizeUrlScript = open('normalize_url.js', 'r').read()

def process_css(content: str, req_context: RequestContext) -> str:
    return re.sub(
            r'url\((.*?)\)',
            lambda matchobj: f'url({spoof_url(matchobj.group(1), req_context)})',
            content)

def process_html(content: bytes, req_context: RequestContext) -> str:
    soup = BeautifulSoup(content, 'html.parser')
    if not soup.head:
        soup.insert(0, soup.new_tag('head'))

    normalize_url_module = soup.new_tag('script')
    normalize_url_module

    corsHandler = soup.new_tag('script')
    corsHandler.string = jsRequestHandler
    soup.head.insert(0, corsHandler)

    for attr in linkAttr:
        for tag in soup.findAll(**linkAttr[attr]):
            tag[attr] = spoof_url(tag[attr], req_context)

    for style in soup.findAll('style'):
        if style.string == None:
            style.string = ''
        style.string = process_css(style.string, req_context)

    return str(soup)
