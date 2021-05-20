from urllib.parse import urlparse


class RequestContext:
    def __init__(self, own_host: str, target_url: str):
        self.own_host = own_host
        self.target_url = target_url
        self.target_parsed = urlparse(target_url)

