from backend import test, movie


class TestMovieApi(test.TestCase):
    def test_get_list(self):
        self.policy.SetProbability(1)
        movie.Movie.create(title="Dog", year=2000, imdb_id="xyz", type="movie", poster_url="http://poster")
        resp = self.api_mock.post("/api/movie.get_list")
        self.assertEqual(resp.get("error"), None)
        self.assertEqual(resp.get("movies"), [{'title': 'Dog'}])
        self.assertIsNotNone(resp.get("offset"))
        self.assertEqual(resp.get("page_size"), 10)

    def test_get_list_pagination(self):
        self.policy.SetProbability(1)
        for i in xrange(ord('A'), ord('H') + 1):
            title = chr(i)
            movie.Movie.create(title=title, year=2000, imdb_id="id" + title, type="movie", poster_url="http://poster")
        resp = self.api_mock.post("/api/movie.get_list", dict(page_size=3))
        self.assertEqual(resp.get("error"), None)
        self.assertEqual(resp.get("movies"), [{'title': 'A'}, {'title': 'B'}, {'title': 'C'}])
        self.assertEqual(resp.get("page_size"), 3)
        resp = self.api_mock.post("/api/movie.get_list", dict(page_size=3, offset=resp.get('offset')))
        self.assertEqual(resp.get("error"), None)
        self.assertEqual(resp.get("movies"), [{'title': 'D'}, {'title': 'E'}, {'title': 'F'}])
        self.assertEqual(resp.get("page_size"), 3)
        resp = self.api_mock.post("/api/movie.get_list", dict(page_size=3, offset=resp.get('offset')))
        self.assertEqual(resp.get("error"), None)
        self.assertEqual(resp.get("movies"), [{'title': 'G'}, {'title': 'H'}])
        self.assertEqual(resp.get("page_size"), 3)

    def test_get_by_title(self):
        self.policy.SetProbability(1)
        movie.Movie.create(title="Dog", year=2000, imdb_id="xyz", type="movie", poster_url="http://poster")
        resp = self.api_mock.post("/api/movie.get_by_title", dict(title="Dog"))
        self.assertEqual(resp.get("error"), None)
        self.assertEqual(resp.get("title"), "Dog")

    def test_get_by_title_not_found(self):
        resp = self.api_mock.post("/api/movie.get_by_title", dict(title="Dog"))
        self.assertIsNotNone(resp.get("error"))

    def test_create_from_omdb(self):
        resp = self.api_mock.post("/api/movie.create_from_omdb", dict(title="Hulk"))
        self.assertEqual(resp.get("title"), "Hulk")
