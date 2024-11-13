from abc import ABCMeta
from utils.context import Context
from utils.logger import Logger
from sqlalchemy.orm import scoped_session


class BaseController(metaclass=ABCMeta):
    def __init__(self, context: Context, class_name: str) -> None:
        self.context: Context = context
        self.session: scoped_session = context.db_session
        self.logger = Logger(context, class_name)
