from datetime import datetime
from abc import ABCMeta
import json
from requests import Response, request

from utils.logger import Logger
from utils.context import Context


class RestConnector(metaclass=ABCMeta):
    def __init__(self, context: Context, class_name, base_url, timeout) -> None:
        self.logger = Logger(context, class_name)
        self.base_url = base_url
        self.context = context
        self.timeout = timeout

    def send(
        self,
        endpoint,
        method,
        payload=None,
        headers=None,
        data=None,
        cert=None,
        verify=True,
        params=None,
        timeout=None,
        hide_incoming_json=False,
        hide_outgoing_json=False,
    ):
        if headers is None:
            headers = {}

        headers["GlobalTraceId"] = self.context.global_trace_id
        url = f"{self.base_url}{endpoint}"

        to_log_json = {}
        if params is not None:
            to_log_json["params"] = params

        if payload is not None and hide_outgoing_json is not True:
            to_log_json["payload"] = payload

        self.logger.info(f"OUTGOING REQUEST {method} {url}", to_log_json)
        start = datetime.utcnow()

        response = request(
            method.upper(),
            url,
            headers=headers,
            json=payload,
            data=data,
            cert=cert,
            params=params,
            verify=verify,
            timeout=timeout,
        )
        end = datetime.utcnow()

        base_response = BaseConnectorResponse(
            endpoint=endpoint,
            method=method,
            payload=payload,
            headers=headers,
            start=start,
            end=end,
            response=response,
        )

        took = (end - start).total_seconds() * 1000

        to_log_json = {"payload": base_response.response_json or base_response.response.text}

        if hide_incoming_json is True:
            to_log_json = "HIDDEN"

        self.logger.info(
            f"INCOMING RESPONSE {response.status_code} {method} {url} {took} ms",
            to_log_json,
        )

        if base_response.response_status >= 300:
            raise BaseConnectorException(base_response)

        return base_response


class BaseConnectorResponse:
    def __init__(
        self,
        response: Response,
        endpoint: str,
        method: str,
        headers: dict,
        payload: dict,
        start: datetime,
        end: datetime,
    ) -> None:
        self.endpoint = endpoint
        self.method = method
        self.payload = payload
        self.headers = headers
        self.start = start
        self.end = end
        self.response = response
        self.response_content = response.content
        self.response_status = response.status_code

        self.response_json = None
        try:
            self.response_json = json.loads(self.response_content)
        except Exception:
            ...
            # logger warning

    def __str__(self):
        return f"Response(method={self.method}, endpoint={self.endpoint}, status={self.response_status})"


class BaseConnectorException(Exception):
    def __init__(self, base_response: BaseConnectorResponse) -> None:
        self.base_response = base_response
