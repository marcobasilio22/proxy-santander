import uuid
from falcon import Request

from utils.context import Context


class ContextCreator:
    def process_request(self, req: Request, resp):
        global_trace_id = req.get_header("GlobalTraceId")
        if global_trace_id is None:
            global_trace_id = str(uuid.uuid4())
        req.context.instance = Context(global_trace_id)
