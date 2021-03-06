import logging

from protorpc.remote import ApplicationError


class Error(ApplicationError):
    def __init__(self, message=None):
        logging.info("%s: %s" % (self.__class__.__name__, message))
        super(Error, self).__init__(message, error_name=self.__class__.__name__)


class NotFound(Error):
    pass
