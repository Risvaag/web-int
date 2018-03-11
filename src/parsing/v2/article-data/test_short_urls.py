import unittest
from short_urls import short_urls

class TestShortUrl(unittest.TestCase):

    def setUp(self):
        pass

    def test_shorten_simple_url(self):
        url = 'http://adressa.no/nyheter/innenriks/2016/10/12/kirkegårder-13630735.ece'
        self.assertEqual(short_urls(url), [
            'https://www.adressa.no/nyheter/innenriks/article13630735.ece',
            'https://www.adressa.no/article13630735.ece'
        ])

    def test_should_shorten_two_word_title(self):
        url = 'https://www.adressa.no/nyheter/innenriks/2016/10/12/Pårørende-kirkegårder-13630735.ece'
        self.assertEqual(short_urls(url), [
            'https://www.adressa.no/nyheter/innenriks/article13630735.ece',
            'https://www.adressa.no/article13630735.ece'
        ])

    def test_should_shorten_two_word_title_with_trailing_slash(self):
        url = 'https://www.adressa.no/nyheter/innenriks/2016/10/12/Pårørende-kirkegårder-13630735.ece/wat'
        self.assertEqual(short_urls(url), [
            'https://www.adressa.no/nyheter/innenriks/article13630735.ece',
            'https://www.adressa.no/article13630735.ece'
        ])

    def test_should_be_the_same_for_short_url_with_section(self):
        self.assertEqual(short_urls('https://www.adressa.no/video/article13979473.ece'), [
            'https://www.adressa.no/video/article13979473.ece',
            'https://www.adressa.no/article13979473.ece'
        ])

    def test_should_only_be_short_for_short_url_without_section(self):
        self.assertEqual(short_urls('https://www.adressa.no/article13979473.ece'), [
            'https://www.adressa.no/article13979473.ece',
        ])

    def test_should_not_find_for_html_urls(self):
        url = 'http://www.adressa.no/100Sport/vintersport/langrenn/Lofshus-trekker-frem-andre-idretter-207977b.html'
        self.assertEqual(short_urls(url), [])


if __name__ == '__main__':
    unittest.main()
