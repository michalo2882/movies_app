# coding: utf8
from backend import test, movie


class MovieTests(test.TestCase):
    def test_create(self):
        obj = movie.Movie.create(title="Dog", year=2000, imdb_id="xyz", type="movie", poster_url="http://poster")
        self.assertEqual(obj, movie.Movie.get(obj.id))
        self.assertEqual("Dog", obj.title)
