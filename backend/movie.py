# coding: utf8

from backend import error
from backend.cache import lru_cache
from google.appengine.ext import ndb


class Movie(ndb.Model):
    title = ndb.StringProperty(indexed=False)
    year = ndb.IntegerProperty(indexed=False)
    imdb_id = ndb.StringProperty(indexed=False)
    type = ndb.StringProperty(indexed=False)
    poster_url = ndb.StringProperty(indexed=False)

    @property
    def id(self):
        return self.key.urlsafe()

    @classmethod
    def create(cls, title, year, imdb_id, type, poster_url):
        entity = cls(title=title, year=year, imdb_id=imdb_id, type=type, poster_url=poster_url)
        entity.put()
        cls.get.lru_set(entity, args=(cls, entity.id))
        return entity

    @classmethod
    @lru_cache()
    def get(cls, pk):
        entity = None

        try:
            entity = ndb.Key(urlsafe=pk).get()
        except:
            pass

        if entity is None or not isinstance(entity, cls):
            raise error.NotFound("No Movie found with id: %s" % pk)

        return entity
