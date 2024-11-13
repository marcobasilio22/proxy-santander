import os
from constants import APP_ENV

from utils.logger import LogHandler

logger = LogHandler().get_logger(__name__)


class SecretsManagerConnector:
    @staticmethod
    def get_secret_by_name(secret_name):
            if APP_ENV.upper() == "LOCAL":
                secret_value = os.getenv(secret_name)
                if secret_value is None:
                    logger.error(f"Secret {secret_name} not found in .env")
                    raise ValueError(f"Secret {secret_name} not found in .env")
                logger.debug(f"Retrieved secret {secret_name} from .env")
                return {"secret_string_value": secret_value}
            else:
                raise NotImplementedError("Secrets retrieval from Secrets Manager is disabled for this environment.")