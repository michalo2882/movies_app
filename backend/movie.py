# coding: utf8

from backend import error
from backend.cache import lru_cache
from google.appengine.ext import ndb


class DuplicateMovieError(error.Error):
    pass


class Movie(ndb.Model):
    title = ndb.StringProperty(indexed=False)
    year = ndb.IntegerProperty(indexed=False)
    imdb_id = ndb.StringProperty(indexed=True)
    type = ndb.StringProperty(indexed=False)
    poster_url = ndb.StringProperty(indexed=False)

    @property
    def id(self):
        return self.key.urlsafe()

    @classmethod
    def create(cls, title, year, imdb_id, type, poster_url):
        if cls.get_by_imdb_id(imdb_id) is not None:
            raise DuplicateMovieError("IMDB id %s is already in db" % imdb_id)

        entity = cls(title=title, year=year, imdb_id=imdb_id, type=type, poster_url=poster_url)
        entity.put()
        cls.get.lru_set(entity, args=(cls, entity.id))
        cls.get_by_imdb_id.lru_set(entity, args=(cls, entity.imdb_id))
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

    @classmethod
    @lru_cache()
    def get_by_imdb_id(cls, imdb_id):
        entities = cls.query(cls.imdb_id == imdb_id).fetch(1)
        return entities[0] if entities else None

    @classmethod
    def get_total_count(cls):
        return cls.query().count()
