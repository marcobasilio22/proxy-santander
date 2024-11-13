from falcon import Request, Response

from utils.security_tools import SecurityTools
from constants import BYPASS_ENDPOINTS


class InternalAuthenticationMiddleware:
    def process_request(self, req: Request, resp: Response):
        if req.method == "OPTIONS" or req.path in BYPASS_ENDPOINTS:
            return
        SecurityTools.validate_internal_request(req)

    def process_response(self, req, resp, resource, req_succeeded):
        if req.method == "OPTIONS" or req.path in BYPASS_ENDPOINTS:
            return
