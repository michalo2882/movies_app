# coding: utf8

from backend import test
from backend.omdb_service import OmdbService


class OmdbServiceTests(test.TestCase):
    def test_fix_year(self):
        self.assertEqual(2020, OmdbService._fix_year('2020'))
        self.assertEqual(2020, OmdbService._fix_year('  2020  '))
        self.assertEqual(2020, OmdbService._fix_year('2020----'))
        self.assertEqual(2020, OmdbService._fix_year('  2020  ----'))
        self.assertEqual(2020, OmdbService._fix_year('  2020  :D'))
        self.assertEqual(None, OmdbService._fix_year(':D'))
