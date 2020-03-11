import httplib2
import json
import re

from backend import movie
from backend.omdb_service import OmdbService


class MovieInitializer(object):
    def __init__(self, omdb_service, count=100):
        """

        @type omdb_service: backend.omdb_service.OmdbService
        """
        self.omdb_service = omdb_service
        self.count = count
        self.search_text = 'love'
        self.year = 2019

    @classmethod
    def execute(cls):
        initializer = cls(OmdbService())
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
            self._persist_movies(movies_raw)
            fetched_count += len(movies_raw)
            page += 1

    def _fetch_movies(self, page):
        return self.omdb_service.fetch_movies(page, self.search_text, self.year)

    def _persist_movies(self, raw_data):
        for entry in raw_data:
            try:
                movie.Movie.create(**entry)
            except movie.DuplicateMovieError:
                pass

    def _get_current_movies_count(self):
        return movie.Movie.get_total_count()
