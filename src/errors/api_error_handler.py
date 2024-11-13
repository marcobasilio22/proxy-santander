import falcon
from falcon import HTTPError
import traceback
import json

from errors.base_error import QIException, MethodNotAllowed, InternalError, InvalidParameter
from utils.logger import Logger


class APIErrorHandler:
    @staticmethod
    def qi_exception(req, resp, ex: QIException, params):
        raise FalconQIException(ex)

    @staticmethod
    def method_not_allowed(req, resp, ex, params):
        raise FalconQIException(MethodNotAllowed())

    @staticmethod
    def invalid_parameter(req, resp, ex: falcon.HTTPInvalidParam, params):
        raise FalconQIException(InvalidParameter(ex.description))

    @staticmethod
    def unexpected(req, resp, ex, params):
        stack_trace_limit = 10
        logger = Logger(req.context.instance, __name__)
        _traceback = traceback.format_exc(stack_trace_limit)
        logger.fatal(_traceback)
        raise FalconQIException(InternalError())


class FalconQIException(HTTPError):
    def __init__(self, qi_exception: QIException):
        HTTPError.__init__(self, getattr(falcon, f"HTTP_{str(qi_exception.http_status)}"))
        self.title = qi_exception.title
        self.description = qi_exception.description
        self.translation = qi_exception.translation
        self.code = qi_exception.code

    def to_dict(self):
        obj = dict()
        obj["title"] = self.title
        obj["description"] = self.description
        obj["translation"] = self.translation
        obj["code"] = self.code

        if self.link is not None:
            obj["link"] = self.link

        return obj

    def to_json(self, *args):
        obj = self.to_dict()
        json_str = json.dumps(obj, ensure_ascii=False)
        return str.encode(json_str)
