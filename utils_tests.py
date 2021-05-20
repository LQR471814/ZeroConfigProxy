import unittest
from common.types import *
from utils.parsing_utils import *

class ParsingUtilsTest(unittest.TestCase):
    def run_test_cases(self, cases: list, func):
        for case in cases:
            actual = func(*case['input'])
            self.assertEqual(
                case['expected'],
                actual,
                'failed test | expected {}, actual {}'.format(
                    case['expected'], actual
                ),
            )

    def test_get_target_url(self):
        test_cases = [
            {
                'input': [urlparse('http://foo.com/Request?targetUrl=http%3A%2F%2Fbar.com%2F')],
                'expected': 'http://bar.com/'
            },
            {
                'input': [urlparse('http://foo.com/path/?targetUrl=http%3A%2F%2Fbar.com%2F%3Fwhowhwoh%3Dabcdefgh')],
                'expected': 'http://bar.com/?whowhwoh=abcdefgh'
            }
        ]
        self.run_test_cases(test_cases, get_target_url)

    def test_spoof_url(self):
        test_cases = [
            {
                'input': [
                    'http://foo.com/PathStuff/?query=yes',
                    RequestContext(
                        own_host='own_host',
                        target_url='https://bar.com/'
                    )
                ],
                'expected': 'http://own_host/Request?targetUrl=http%3A%2F%2Ffoo.com%2FPathStuff%2F%3Fquery%3Dyes'
            },
            {
                'input': [
                    'portal/wikipedia.org/assets/img/sprite-d7502d35.svg',
                    RequestContext(
                        own_host='own_host',
                        target_url='https://www.wikipedia.com/'
                    )
                ],
                'expected': 'http://own_host/Request?targetUrl=https%3A%2F%2Fwww.wikipedia.com%2Fportal%2Fwikipedia.org%2Fassets%2Fimg%2Fsprite-d7502d35.svg'
            },
            {
                'input': [
                    'www.google.com/image.png',
                    RequestContext(
                        own_host='own_host',
                        target_url='https://www.google.com/'
                    )
                ],
                'expected': 'http://own_host/Request?targetUrl=https%3A%2F%2Fwww.google.com%2Fimage.png'
            },
            {
                'input': [
                    '//wikimediafoundation.org/',
                    RequestContext(
                        own_host='own_host',
                        target_url='https://wikipedia.com/'
                    )
                ],
                'expected': 'http://own_host/Request?targetUrl=https%3A%2F%2Fwikimediafoundation.org%2F'
            }
        ]
        self.run_test_cases(test_cases, spoof_url)
