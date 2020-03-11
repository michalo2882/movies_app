from backend import api, movie, omdb_service
from backend.error import NotFound
from backend.oauth2 import oauth2
from protorpc import remote, message_types, messages


class MovieListRequest(messages.Message):
    offset = messages.StringField(1)
    page_size = messages.IntegerField(2)


class GetMovieByTitleRequest(messages.Message):
    title = messages.StringField(1)


class GetMovieByIdRequest(messages.Message):
    id = messages.StringField(1)


class MovieResponse(messages.Message):
    title = messages.StringField(1)


class MovieListResponse(messages.Message):
    movies = messages.MessageField(MovieResponse, 1, repeated=True)
    offset = messages.StringField(2)
    page_size = messages.IntegerField(3)


@api.endpoint(path="movie", title="Movie API")
class Movie(remote.Service):

    @remote.method(MovieListRequest, MovieListResponse)
    def get_list(self, request):
        page_size = request.page_size or 10
        result, cursor, has_next = movie.Movie.get_many(page_size, request.offset)
        movies = [MovieResponse(title=m.title) for m in result]
        return MovieListResponse(movies=movies, offset=cursor, page_size=page_size)

    @remote.method(GetMovieByTitleRequest, MovieResponse)
    def get_by_title(self, request):
        obj = movie.Movie.get_by_title(request.title)
        if not obj:
            raise NotFound()
        return MovieResponse(title=obj.title)

    @remote.method(GetMovieByTitleRequest, MovieResponse)
    def create_from_omdb(self, request):
        obj = movie.Movie.create_from_omdb(request.title, omdb_service.OmdbService())
        return MovieResponse(title=obj.title)

    @oauth2.required()
    @remote.method(GetMovieByIdRequest, message_types.VoidMessage)
    def delete_by_id(self, request):
        movie.Movie.get(request.id).delete()
        return message_types.VoidMessage()
