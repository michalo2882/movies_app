# coding: utf8
from mock import MagicMock

from backend import test
from backend.omdb_service import OmdbService, TitleNotFoundError


class OmdbServiceTests(test.TestCase):
    def test_fix_year(self):
        self.assertEqual(2020, OmdbService._fix_year('2020'))
        self.assertEqual(2020, OmdbService._fix_year('  2020  '))
        self.assertEqual(2020, OmdbService._fix_year('2020----'))
        self.assertEqual(2020, OmdbService._fix_year('  2020  ----'))
        self.assertEqual(2020, OmdbService._fix_year('  2020  :D'))
        self.assertEqual(None, OmdbService._fix_year(':D'))

    def test_fetch_by_title(self):
        service = OmdbService()
        service.client = MagicMock()
        service.client.request = MagicMock(return_value=(None, '''
        {
            "Title": "Dog",
            "Year": "2000",
            "imdbID": "abc",
            "Type": "type",
            "Poster": "some uri",
            "Response": true
        }
        '''))
        record = service.fetch_by_title("Dog")
        self.assertEqual("Dog", record['title'])
        self.assertEqual(2000, record['year'])
        self.assertEqual("abc", record['imdb_id'])
        self.assertEqual("type", record['type'])
        self.assertEqual("some uri", record['poster_url'])

    def test_fetch_by_title_not_found(self):
        service = OmdbService()
        service.client = MagicMock()
        service.client.request = MagicMock(return_value=(None, '''
        {
            "Response": false
        }
        '''))
        self.assertRaises(TitleNotFoundError, lambda: service.fetch_by_title("Dog"))
