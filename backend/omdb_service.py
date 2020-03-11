import json
import re

import httplib2


class OmdbService(object):
    def __init__(self):
        self.api_key = 'd6539b9a'
        self.client = httplib2.Http()

    def fetch_movies(self, page, search_text, year):
        client = httplib2.Http()
        resp, content = client.request("http://www.omdbapi.com/?apikey={}&s={}&y={}&page={}".format(
            self.api_key, search_text, year, page), "GET")
        result = json.loads(content)
        return [self._transform_record(r) for r in result['Search']], result['totalResults']

    @classmethod
    def _transform_record(cls, record):
        return {
            'title': record['Title'],
            'year': cls._fix_year(record['Year']),
            'imdb_id': record['imdbID'],
            'type': record['Type'],
            'poster_url': record['Poster'],
        }

    @classmethod
    def _fix_year(cls, year_raw):
        year_raw = year_raw.strip()
        match = re.search(r'[0-9]+', year_raw)
        return int(match.group()) if match else None
