import unittest
from crazy_urls import crazy_urls

class TestUM(unittest.TestCase):

    def setUp(self):
        pass

    def test_should_capitalize_one_word_title(self):
        url = 'http://adressa.no/nyheter/innenriks/2016/10/12/kirkegårder-13630735.ece'
        self.assertCountEqual(crazy_urls(url), [
            'http://adressa.no/nyheter/innenriks/2016/10/12/kirkegårder-13630735.ece',
            'http://adressa.no/nyheter/innenriks/2016/10/12/Kirkegårder-13630735.ece',
        ])

    def test_should_capitalize_two_word_title(self):
        url = 'https://www.adressa.no/nyheter/innenriks/2016/10/12/Pårørende-kirkegårder-13630735.ece'
        self.assertCountEqual(crazy_urls(url), [
            'https://www.adressa.no/nyheter/innenriks/2016/10/12/pårørende-kirkegårder-13630735.ece',
            'https://www.adressa.no/nyheter/innenriks/2016/10/12/Pårørende-kirkegårder-13630735.ece',
            'https://www.adressa.no/nyheter/innenriks/2016/10/12/pårørende-Kirkegårder-13630735.ece',
            'https://www.adressa.no/nyheter/innenriks/2016/10/12/Pårørende-Kirkegårder-13630735.ece'
        ])

    def test_should_capitalize_two_word_title_with_trailing_slash(self):
        url = 'https://www.adressa.no/nyheter/innenriks/2016/10/12/Pårørende-kirkegårder-13630735.ece/wat'
        self.assertCountEqual(crazy_urls(url), [
            'https://www.adressa.no/nyheter/innenriks/2016/10/12/pårørende-kirkegårder-13630735.ece/wat',
            'https://www.adressa.no/nyheter/innenriks/2016/10/12/Pårørende-kirkegårder-13630735.ece/wat',
            'https://www.adressa.no/nyheter/innenriks/2016/10/12/pårørende-Kirkegårder-13630735.ece/wat',
            'https://www.adressa.no/nyheter/innenriks/2016/10/12/Pårørende-Kirkegårder-13630735.ece/wat'
        ])

    def test_should_capitalize_three_word_title(self):
        url = 'https://www.adressa.no/pluss/okonomi/2016/12/11/teller-ikke-arbeidstimer-13911735.ece'
        self.assertCountEqual(crazy_urls(url), [
            'https://www.adressa.no/pluss/okonomi/2016/12/11/teller-ikke-arbeidstimer-13911735.ece',
            'https://www.adressa.no/pluss/okonomi/2016/12/11/teller-ikke-Arbeidstimer-13911735.ece',
            'https://www.adressa.no/pluss/okonomi/2016/12/11/teller-Ikke-arbeidstimer-13911735.ece',
            'https://www.adressa.no/pluss/okonomi/2016/12/11/teller-Ikke-Arbeidstimer-13911735.ece',
            'https://www.adressa.no/pluss/okonomi/2016/12/11/Teller-ikke-arbeidstimer-13911735.ece',
            'https://www.adressa.no/pluss/okonomi/2016/12/11/Teller-ikke-Arbeidstimer-13911735.ece',
            'https://www.adressa.no/pluss/okonomi/2016/12/11/Teller-Ikke-arbeidstimer-13911735.ece',
            'https://www.adressa.no/pluss/okonomi/2016/12/11/Teller-Ikke-Arbeidstimer-13911735.ece',
        ])

    def test_should_be_nothing_for_short_url(self):
        self.assertEqual(crazy_urls('https://www.adressa.no/video/article13979473.ece'), [])

    def test_should_not_find_for_html_urls(self):
        self.assertEqual(crazy_urls('http://www.adressa.no/100Sport/vintersport/langrenn/Lofshus-avviser-ukultur-i-langrenn-og-trekker-frem-andre-idretter-207977b.html'), [])

    def test_should_not_shorten_really_title(self):
        url = 'https://www.adressa.no/nyheter/innenriks/2016/10/12/Dette-er-en-veldig-lang-tittel-som-vi-ikke-kan-være-crazy-med-13630735.ece'
        self.assertEqual(crazy_urls(url), [])

if __name__ == '__main__':
    unittest.main()
