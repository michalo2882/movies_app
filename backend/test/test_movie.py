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

    def test_get_many(self):
        self.policy.SetProbability(1)
        for i in xrange(ord('A'), ord('H') + 1):
            title = chr(i)
            movie.Movie.create(title=title, year=2000, imdb_id="id" + title, type="movie", poster_url="http://poster")

        result, next_cursor, has_more = movie.Movie.get_many(3, start=None)
        self.assertEqual(3, len(result))
        self.assertEqual('A', result[0].title)
        self.assertEqual('B', result[1].title)
        self.assertEqual('C', result[2].title)
        self.assertIsNotNone(next_cursor)
        self.assertTrue(has_more)

        result, next_cursor, has_more = movie.Movie.get_many(3, start=next_cursor)
        self.assertEqual(3, len(result))
        self.assertEqual('D', result[0].title)
        self.assertEqual('E', result[1].title)
        self.assertEqual('F', result[2].title)
        self.assertIsNotNone(next_cursor)
        self.assertTrue(has_more)

        result, _, _ = movie.Movie.get_many(3, start=next_cursor)
        self.assertEqual(2, len(result))
        self.assertEqual('G', result[0].title)
        self.assertEqual('H', result[1].title)
