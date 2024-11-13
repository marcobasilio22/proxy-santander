from errors.base_error import ForbiddenNotInternal
from connectors.secrets_manager_connector import SecretsManagerConnector


from utils.logger import LogHandler

from falcon import Request

logger = LogHandler().get_logger(__name__)

class ThisTokenCache:
    internal_token = None

class SecurityTools:
    @staticmethod
    def validate_internal_request(req: Request) -> None:
        internal_token_value = ThisTokenCache.internal_token
        is_cached = True
        if internal_token_value is None:
            internal_token_value = SecretsManagerConnector.get_secret_by_name("SANTANDER_PROXY_INTERNAL_TOKEN_SECRET_NAME")[
                "secret_string_value"
            ]
            ThisTokenCache.internal_token = internal_token_value
            is_cached = False

        given_internal_token = req.headers.get("INTERNAL-TOKEN")
        if internal_token_value != given_internal_token and is_cached:
            internal_token_value = SecretsManagerConnector.get_secret_by_name("SANTANDER_PROXY_INTERNAL_TOKEN_SECRET_NAME")[
                "secret_string_value"
            ]
            ThisTokenCache.internal_token = internal_token_value

        if internal_token_value != given_internal_token:
            raise ForbiddenNotInternal()
