import re

from bs4 import BeautifulSoup
from common.html_definitions import *
from common.types import *
from utils.parsing_utils import *

jsRequestHandlerScript = open('request_handler.js', 'r').read()
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
    normalize_url_module.string = normalizeUrlScript
    soup.head.insert(0, normalize_url_module)

    jsRequestHandler = soup.new_tag('script')
    jsRequestHandler.string = jsRequestHandlerScript
    soup.head.insert(0, jsRequestHandler)

    for searchObj in linkAttr:
        for tag in soup.findAll(**searchObj):
            for attr in searchObj:
                tag[attr] = spoof_url(tag[attr], req_context)
            if tag.name == 'img':
                if tag.get('srcset'):
                    del tag['srcset']

    for style in soup.findAll('style'):
        if style.string == None:
            style.string = ''
        style.string = process_css(style.string, req_context)

    return str(soup)
