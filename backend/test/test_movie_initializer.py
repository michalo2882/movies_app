# coding: utf8
from mock import MagicMock, call, ANY

from backend import test
from backend.movie_initializer import MovieInitializer


class MovieInitializerTests(test.TestCase):
    def setUp(self):
        super(MovieInitializerTests, self).setUp()
        self.omdb_service = MagicMock()

    def test_is_initialized(self):
        initializer = MovieInitializer(self.omdb_service)
        initializer._get_current_movies_count = MagicMock(return_value=0)
        self.assertFalse(initializer.is_initialized())
        initializer._get_current_movies_count = MagicMock(return_value=5)
        self.assertTrue(initializer.is_initialized())

    def test_fetch_movies_when_source_has_exactly_requested_movies_count(self):
        initializer = MovieInitializer(self.omdb_service, 20)
        self.omdb_service.fetch_movies = MagicMock(return_value=(range(10), 20))
        initializer._persist_movies = MagicMock()
        initializer.download_movies_data()
        self.omdb_service.fetch_movies.assert_has_calls([call(1, ANY, ANY), call(2, ANY, ANY)])

    def test_fetch_movies_when_source_has_more_than_requested_movies_count(self):
        initializer = MovieInitializer(self.omdb_service, 20)
        self.omdb_service.fetch_movies = MagicMock(return_value=(range(10), 100))
        initializer._persist_movies = MagicMock()
        initializer.download_movies_data()
        self.omdb_service.fetch_movies.assert_has_calls([call(1, ANY, ANY), call(2, ANY, ANY)])

    def test_fetch_movies_when_source_has_less_than_requested_movies_count(self):
        initializer = MovieInitializer(self.omdb_service, 100)
        self.omdb_service.fetch_movies = MagicMock(return_value=(range(10), 15))
        initializer._persist_movies = MagicMock()
        initializer.download_movies_data()
        self.omdb_service.fetch_movies.assert_has_calls([call(1, ANY, ANY), call(2, ANY, ANY)])
