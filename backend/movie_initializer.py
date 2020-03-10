import httplib2
import json
import re

from backend import movie


class MovieInitializer(object):
    def __init__(self, count=100):
        self.count = count
        self.api_key = 'd6539b9a'
        self.search_text = 'love'
        self.year = 2019

    @classmethod
    def execute(cls):
        initializer = cls()
        if not initializer.is_initialized():
            initializer.download_movies_data()

    def is_initialized(self):
        return self._get_current_movies_count() > 0

    def download_movies_data(self):
        count = self.count
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
        client = httplib2.Http()
        resp, content = client.request("http://www.omdbapi.com/?apikey={}&s={}&y={}&page={}".format(
            self.api_key, self.search_text, self.year, page), "GET")
        result = json.loads(content)
        return result['Search'], result['totalResults']

    def _persist_movies(self, raw_data):
        for entry in raw_data:
            try:
                movie.Movie.create(title=entry['Title'], year=self.fix_year(entry['Year']), imdb_id=entry['imdbID'],
                                   type=entry['Type'], poster_url=entry['Poster'])
            except movie.DuplicateMovieError:
                pass

    def _get_current_movies_count(self):
        return movie.Movie.get_total_count()

    @classmethod
    def fix_year(cls, year_raw):
        year_raw = year_raw.strip()
        match = re.search(r'[0-9]+', year_raw)
        return int(match.group()) if match else None
