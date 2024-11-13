from connectors.rest_connector import (
    RestConnector,
    BaseConnectorResponse,
)
from models.tokens_entity import Tokens
from utils.context import Context
from utils.validate import ValidationToken

from constants import (
    SANTANDER_ACCOUNT_API_URL, 
    SANTANDER_ACCOUNT_SIGNED_CERTIFICATE,
    SANTANDER_CONSULT_CLIENT_ID
)

class SantanderBankConnector(RestConnector):
    def __init__(self, context: Context) -> None:
        super().__init__(context, __name__, base_url=SANTANDER_ACCOUNT_API_URL, timeout=60)
        self.rest_connector = RestConnector(context, __name__, base_url=SANTANDER_ACCOUNT_API_URL, timeout=60)

    def generate_token(self):
        self.tokens = Tokens()
        lastToken = self.tokens.get_last_token('consult')
        
        if lastToken:
            token_string = lastToken.token  
        else:
            token_string = None
        
        return token_string
        
    def __create_header(self, bank_client_id:str):
        self.token_validator = ValidationToken()
        self.token_validator.validation_consult_token()
        token = self.generate_token()
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "X-Application-Key": bank_client_id,
        }

        return headers

    def get_account_balance(
            self, 
            bankdoc:str,
            bankaccount:str,
        ) -> BaseConnectorResponse: 
        
        header = self.__create_header(SANTANDER_CONSULT_CLIENT_ID)
        
        response = self.send(
            endpoint=f"/bank_account_information/v1/banks/{bankdoc}/balances/{bankaccount}",
            method="GET",
            headers=header,
            cert=SANTANDER_ACCOUNT_SIGNED_CERTIFICATE
        )
        
        status = response.response_status    
                
        if status != 200:
            raise Exception(f"Error in consult balance: {status}")

        return response.response_json, status
    
    def get_extract_account(
            self,
            bankdoc:str, 
            start_date:str, 
            end_date:str, 
            bankaccount:str
        ) -> BaseConnectorResponse:
        
        headers = self.__create_header(SANTANDER_CONSULT_CLIENT_ID)
        
        params = {
            "_offset": 1,
            "_limit": 100,
            "initialDate": start_date,
            "finalDate": end_date,
        }

        response = self.send(
            endpoint=f"/bank_account_information/v1/banks/{bankdoc}/statements/{bankaccount}",
            method="GET",
            params=params,
            headers=headers,
            cert=SANTANDER_ACCOUNT_SIGNED_CERTIFICATE
        )

        status = response.response_status    
                
        if status != 200:
            raise Exception(f"Error in consult extract: {status}")

        return response.response_json, status