# coding: utf8
from mock import MagicMock, call

from backend import test, movie
from backend.movie_initializer import MovieInitializer


class MovieInitializerTests(test.TestCase):
    def test_get_movies_to_fetch_count(self):
        initializer = MovieInitializer(max_movies_count=10)
        initializer._get_current_movies_count = MagicMock(return_value=4)
        self.assertEqual(6, initializer.get_movies_to_fetch_count())
        initializer._get_current_movies_count = MagicMock(return_value=50)
        self.assertEqual(0, initializer.get_movies_to_fetch_count())

    def test_fetch_movies_when_source_has_exactly_requested_movies_count(self):
        initializer = MovieInitializer()
        initializer._fetch_movies = MagicMock(return_value=(range(10), 20))
        initializer._persist_movies = MagicMock()
        initializer.download_movies_data(20)
        initializer._fetch_movies.assert_has_calls([call(1), call(2)])

    def test_fetch_movies_when_source_has_more_than_requested_movies_count(self):
        initializer = MovieInitializer()
        initializer._fetch_movies = MagicMock(return_value=(range(10), 100))
        initializer._persist_movies = MagicMock()
        initializer.download_movies_data(20)
        initializer._fetch_movies.assert_has_calls([call(1), call(2)])

    def test_fetch_movies_when_source_has_less_than_requested_movies_count(self):
        initializer = MovieInitializer()
        initializer._fetch_movies = MagicMock(return_value=(range(10), 15))
        initializer._persist_movies = MagicMock()
        initializer.download_movies_data(100)
        initializer._fetch_movies.assert_has_calls([call(1), call(2)])
