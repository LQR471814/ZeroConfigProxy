linkAttr = {
    'href': {
        'href': True
    },
    'src': {
        'src': True
    },
    'action': {
        'action': True
    },
    'data': {
        'data': True
    },
    'profile': {
        'profile': True
    },
    'cite': {
        'cite': True
    },
    'classid': {
        'classid': True
    },
    'codebase': {
        'codebase': True
    },
    'usemap': {
        'usemap': True
    },
    'formaction': {
        'formaction': True
    },
    'icon': {
        'icon': True
    },
    'manifest': {
        'manifest': True
    },
    'poster': {
        'poster': True
    },
    'content': {
        'content':
        True,  # ? To catch the Open Graph Protocol and some twitter metadata exhibited in <meta> tags, see https://ogp.me/
        'property':
        lambda inp: inp == 'og:url' or inp == 'og:image' or inp == 'og:audio'
        or inp == 'og:video' or inp == 'og:image:secure_url' or inp ==
        'twitter:image'
    }
}

HTTP_METHODS = [
    'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE',
    'PATCH'
]
