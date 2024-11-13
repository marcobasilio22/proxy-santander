import logging
import sys
import json

from utils.singleton import Singleton
from utils.context import Context
from utils.decimal_encoder import DecimalEncoder

from constants import SERVICE_NAME, APP_ENV

logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)


class Logger:
    def __init__(self, context: Context, class_name):
        self.context = context
        self.handler = LogHandler().get_logger(class_name)

    def debug(self, msg, message_json=None):
        log_json = self.__prepare_log(msg, message_json)
        self.handler.debug(log_json)

    def info(self, msg, message_json=None):
        log_json = self.__prepare_log(msg, message_json)
        self.handler.info(log_json)

    def warning(self, msg, message_json=None):
        log_json = self.__prepare_log(msg, message_json)
        self.handler.warning(log_json)

    def error(self, msg, message_json=None):
        log_json = self.__prepare_log(msg, message_json)
        self.handler.error(log_json)

    def fatal(self, msg, message_json=None):
        log_json = self.__prepare_log(msg, message_json)
        self.handler.fatal(log_json)

    def __prepare_log(self, msg, message_json):
        if APP_ENV.upper() in ["LOCAL", "TEST"]:
            message = f"{msg}"
            if message_json is not None:
                message_json_str = json.dumps(message_json, cls=DecimalEncoder, default=str)
                message = f"{msg} - {message_json_str}"
            return message

        log_json = dict()

        log_json["message"] = msg
        log_json["global_trace_id"] = self.context.global_trace_id
        log_json["operations"] = self.context.operations

        if message_json is not None:
            log_json["message_json"] = message_json

        return json.dumps(log_json, cls=DecimalEncoder, default=str)


class LogHandler(metaclass=Singleton):
    def __init__(self) -> None:
        self.__setup_root_logger()

    def get_logger(self, class_name):
        logger_name = f"{SERVICE_NAME}.{class_name}"
        logger = logging.getLogger(logger_name)
        return logger

    def __setup_root_logger(self):
        logger = logging.getLogger()
        log_level = logging.DEBUG
        logger.setLevel(log_level)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        formatter = QIFormatter(
            {
                "level": "levelname",
                "message": "message",
                "loggerName": "name",
                "pid": "process",
                "tid": "thread",
                "timestamp": "asctime",
            }
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)


class QIFormatter(logging.Formatter):
    def __init__(
        self,
        fmt_dict: dict = None,
        time_format: str = "%Y-%m-%dT%H:%M:%S",
        msec_format: str = "%s.%03dZ",
    ):
        self.fmt_dict = fmt_dict if fmt_dict is not None else {"message": "message"}
        self.default_time_format = time_format
        self.default_msec_format = msec_format
        self.datefmt = None

    def usesTime(self) -> bool:
        return "asctime" in self.fmt_dict.values()

    def formatMessage(self, record) -> dict:
        return {fmt_key: record.__dict__[fmt_val] for fmt_key, fmt_val in self.fmt_dict.items()}

    def format(self, record) -> str:
        record.message = record.getMessage()

        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        message_dict = self.formatMessage(record)

        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)

        if record.exc_text:
            message_dict["exc_info"] = record.exc_text

        if record.stack_info:
            message_dict["stack_info"] = self.formatStack(record.stack_info)

        pid = message_dict["pid"]
        tid = message_dict["tid"]
        loggerName = message_dict["loggerName"]
        levelName = message_dict["level"]

        try:
            message = json.loads(message_dict["message"])
        except Exception:
            message = message_dict["message"]

        message_dict["message"] = message

        if APP_ENV.upper() in ["LOCAL", "TEST"]:
            return f"{pid} - {tid} [{loggerName}][{levelName}] - {message}"

        return json.dumps(message_dict, default=str)
