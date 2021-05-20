from urllib.parse import (ParseResult, parse_qs, quote, urlencode, urlparse,
                          urlunparse)

from common.types import RequestContext

# ? Technically 'urlencode' takes care of this already but it has some limitations
def qs_encode(dictionary: dict) -> str:
    qsParts = []
    for key in dictionary:
        qsParts.append(f'{key}={dictionary[key]}')
    return '&'.join(qsParts)


def escape_url_for_qs(url: str) -> str:
    return quote(url, safe='')


def get_target_url(url: ParseResult) -> str:
    parsed_query = parse_qs(url.query)

    targetDomain = parsed_query.get('targetUrl')
    if targetDomain:
        # ? For some reason, returns a string
        targetDomain = targetDomain[0]

    return targetDomain


def set_target_url(url: ParseResult, targetUrl: str) -> ParseResult:
    parsed_query = parse_qs(url.query)
    parsed_query['targetUrl'] = targetUrl

    return url._replace(query=urlencode(parsed_query))


def remove_target_url(url: ParseResult) -> ParseResult:
    parsed_query = parse_qs(url.query)
    parsed_query.pop('targetUrl')

    return url._replace(query=urlencode(parsed_query))


# * Point url towards spoof server
def spoof_url(url: str, req_context: RequestContext) -> str:
    default_domain = req_context.target_parsed.netloc
    default_scheme = req_context.target_parsed.scheme

    def normalize_url(target_url: str):
        result = target_url
        result.replace('www.', '') #? Remove www.
        if result.split('/')[0] == default_domain: #? Check if first segment of 'path' is the default_domain
            result = f'{default_scheme}://' + result #? Add http(s):// in front if it is a url like (www.google.com/path)
        return result

    targetUrl = urlparse(normalize_url(url))

    if targetUrl.scheme == '':
        targetUrl = targetUrl._replace(scheme=default_scheme)
    if targetUrl.netloc == '':
        targetUrl = targetUrl._replace(netloc=default_domain)

    spoofedTargetURL = urlunparse(targetUrl)

    spoofedURL = ParseResult(
        scheme='http', #? Always use http cause' I can't be bothered to run out and get a certificate
        netloc=req_context.own_host,
        path='/Request',
        query=qs_encode({
            'targetUrl': escape_url_for_qs(spoofedTargetURL)
        }),
        params=targetUrl.params,
        fragment=targetUrl.fragment
    )

    return urlunparse(spoofedURL)
