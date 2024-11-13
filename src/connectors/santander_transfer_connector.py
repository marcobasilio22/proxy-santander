from connectors.rest_connector import (
    RestConnector,
    BaseConnectorResponse,
)
from models.tokens_entity import Tokens
from utils.context import Context
from utils.validate import ValidationToken

from constants import (
    SANTANDER_TRANSFER_API_URL, 
    SANTANDER_ACCOUNT_SIGNED_CERTIFICATE,
    SANTANDER_WORKSPACE_URL,
    SANTANDER_TRANSFER_CLIENT_ID
)

class SantanderBankConnector(RestConnector):
    def __init__(self, context: Context) -> None:
        super().__init__(context, __name__, base_url=SANTANDER_TRANSFER_API_URL, timeout=60)
        self.rest_connector = RestConnector(context, __name__, base_url=SANTANDER_TRANSFER_API_URL, timeout=60)

    def generate_token(self):
        self.tokens = Tokens()
        last_token = self.tokens.get_last_token('pix')
        
        if last_token:
            token_string = last_token.token  
        else:
            token_string = None
        
        return token_string

    def __create_header(self, bank_client_id: str):
        self.token_validator = ValidationToken()
        self.token_validator.validation_transfer_token()
        token = self.generate_token()
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "X-Application-Key": bank_client_id,
        }

        return headers

    def post_workspace(
            self,
            branchD:str,
            numberD:str
        )-> BaseConnectorResponse:
        
        headers = self.__create_header(SANTANDER_TRANSFER_CLIENT_ID)
        
        payload = {
                "type": "PAYMENTS",
                "description": "Transfer",
                "mainDebitAccount": {
                    "branch": str(branchD),
                    "number": str(numberD)
                },

                "pixPaymentsActive": True,
                "barCodePaymentsActive": True,
                "bankSlipPaymentsActive": True,
                "bankSlipAvailableActive": True,
                "taxesByFieldPaymentsActive": True,
                "vehicleTaxesPaymentsActive": True
        }
        
        response = self.send(
            endpoint=SANTANDER_WORKSPACE_URL,
            method="POST",
            headers=headers,
            payload=payload,
            cert=SANTANDER_ACCOUNT_SIGNED_CERTIFICATE
        )
    
        status = response.response_status

        return response.response_json, status
    
    def post_payment(
            self,
            workspace_id:str,
            branchB:str,
            numberB:str,
            typep:str,
            document_type:str,
            document_number:str,
            name:str,
            bank_code:str,
            payment_value:str
        )-> BaseConnectorResponse:
        
        headers = self.__create_header(SANTANDER_TRANSFER_CLIENT_ID)
        
        payload = {
            "remittanceInformation": "string",
            "beneficiary": {
                "branch": str(branchB),
                "number": str(numberB),
                "type": typep,
                "documentType": document_type,
                "documentNumber": document_number,
                "name": name,
                "bankCode": bank_code
            },
            "paymentValue": payment_value
            } 
        
        response = self.send(
            endpoint=f"{SANTANDER_WORKSPACE_URL}/{workspace_id}/pix_payments",
            method="POST",
            headers=headers,
            payload=payload,
            cert=SANTANDER_ACCOUNT_SIGNED_CERTIFICATE
        )

        status = response.response_status
        
        return response.response_json, status


    def patch_make_payment(
        self,
        workspace_id:str,
        transfer_id:str,
        payment_value:str
    )-> BaseConnectorResponse:
        
        headers = self.__create_header(SANTANDER_TRANSFER_CLIENT_ID)
        
        payload = {
            "paymentValue": str(payment_value),
            "status": "AUTHORIZED"
        }
        
        response = self.send(
            endpoint=f"{SANTANDER_WORKSPACE_URL}/{workspace_id}/pix_payments/{transfer_id}",
            method="PATCH",
            headers=headers,
            payload=payload,
            cert=SANTANDER_ACCOUNT_SIGNED_CERTIFICATE
        )

        status = response.response_status
        
        return response.response_json, status