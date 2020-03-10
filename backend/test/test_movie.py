# coding: utf8
from backend import test, movie


class MovieTests(test.TestCase):
    def test_create(self):
        obj = movie.Movie.create(title="Dog", year=2000, imdb_id="xyz", type="movie", poster_url="http://poster")
        self.assertEqual(obj, movie.Movie.get(obj.id))
        self.assertEqual("Dog", obj.title)
        self.assertEqual(2000, obj.year)
        self.assertEqual("xyz", obj.imdb_id)
        self.assertEqual("movie", obj.type)
        self.assertEqual("http://poster", obj.poster_url)

    def test_create_duplicate(self):
        movie.Movie.create(title="Dog", year=2000, imdb_id="xyz", type="movie", poster_url="http://poster")
        self.assertRaises(movie.DuplicateMovieError,
                          lambda: movie.Movie.create(title="Dog", year=2000, imdb_id="xyz",
                                                     type="movie", poster_url="http://poster"))

    def test_get_total_count(self):
        self.policy.SetProbability(1)
        movie.Movie.create(title="Dog", year=2000, imdb_id="xyz", type="movie", poster_url="http://poster")
        movie.Movie.create(title="Cat", year=2000, imdb_id="abc", type="movie", poster_url="http://poster")
        self.assertEqual(2, movie.Movie.get_total_count())
