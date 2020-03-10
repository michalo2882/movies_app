# coding: utf8
from mock import MagicMock, call

from backend import test, movie
from backend.movie_initializer import MovieInitializer


class MovieInitializerTests(test.TestCase):
    def test_is_initialized(self):
        initializer = MovieInitializer()
        initializer._get_current_movies_count = MagicMock(return_value=0)
        self.assertFalse(initializer.is_initialized())
        initializer._get_current_movies_count = MagicMock(return_value=5)
        self.assertTrue(initializer.is_initialized())

    def test_fetch_movies_when_source_has_exactly_requested_movies_count(self):
        initializer = MovieInitializer(20)
        initializer._fetch_movies = MagicMock(return_value=(range(10), 20))
        initializer._persist_movies = MagicMock()
        initializer.download_movies_data()
        initializer._fetch_movies.assert_has_calls([call(1), call(2)])

    def test_fetch_movies_when_source_has_more_than_requested_movies_count(self):
        initializer = MovieInitializer(20)
        initializer._fetch_movies = MagicMock(return_value=(range(10), 100))
        initializer._persist_movies = MagicMock()
        initializer.download_movies_data()
        initializer._fetch_movies.assert_has_calls([call(1), call(2)])

    def test_fetch_movies_when_source_has_less_than_requested_movies_count(self):
        initializer = MovieInitializer(100)
        initializer._fetch_movies = MagicMock(return_value=(range(10), 15))
        initializer._persist_movies = MagicMock()
        initializer.download_movies_data()
        initializer._fetch_movies.assert_has_calls([call(1), call(2)])

    def test_fix_year(self):
        self.assertEqual(2020, MovieInitializer.fix_year('2020'))
        self.assertEqual(2020, MovieInitializer.fix_year('  2020  '))
        self.assertEqual(2020, MovieInitializer.fix_year('2020----'))
        self.assertEqual(2020, MovieInitializer.fix_year('  2020  ----'))
        self.assertEqual(2020, MovieInitializer.fix_year('  2020  :D'))
        self.assertEqual(None, MovieInitializer.fix_year(':D'))
