import requests

from backend import movie


class MovieInitializer(object):
    def __init__(self, max_movies_count=100):
        self.max_movies_count = max_movies_count
        self.api_key = 'd6539b9a'
        self.search_text = 'love'
        self.year = 2019

    @classmethod
    def execute(cls):
        initializer = cls()
        count = initializer.get_movies_to_fetch_count()
        initializer.download_movies_data(count)

    def get_movies_to_fetch_count(self):
        total_count = self._get_current_movies_count()
        if total_count >= self.max_movies_count:
            return 0
        else:
            return self.max_movies_count - total_count

    def download_movies_data(self, count):
        page = 1
        fetched_count = 0
        while fetched_count < count:
            movies_raw, total_results = self._fetch_movies(page)
            if total_results < count:
                count = total_results
            movies_raw, _ = self._fetch_movies(page)
            self._persist_movies(movies_raw)
            fetched_count += len(movies_raw)
            page += 1

    def _fetch_movies(self, page):
        result = requests.get("http://www.omdbapi.com/?apikey={}&s={}&y={}&page={}".format(
            self.api_key, self.search_text, self.year, page)).json()
        return result['Search'], result['totalResults']

    def _persist_movies(self, raw_data):
        for entry in raw_data:
            movie.Movie.create(title=entry['Title'], year=entry['Year'], imdb_id=entry['imdbID'],
                               type=entry['Type'], poster_url=entry['Poster'])

    def _get_current_movies_count(self):
        return movie.Movie.get_total_count()
