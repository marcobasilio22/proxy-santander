from connectors.santander_account_connector import SantanderBankConnector
from controllers.base_controller import BaseController
from models.balance_entity import Balance
from models.extracts_entity import Extracts
from models.requests_entity import Requests
from utils.context import Context

class AccountController(BaseController):
    def __init__(self, context: Context) -> None:
        super().__init__(context, __name__)
        self.balance = Balance()
        self.extract = Extracts()
        self.requests = Requests()
        self.santander_bank_statement_connector = SantanderBankConnector(context)

    def get_account_balance(self, bankdoc:str, branchCode:str, accountnumber:str):
        bankaccount = f"{branchCode:04}.{accountnumber:07}"
        response_json, status = self.santander_bank_statement_connector.get_account_balance(bankdoc=bankdoc,
                                                                                            bankaccount=bankaccount)

        balance_value = response_json.get('availableAmount')
        
        if balance_value is None:
            raise ValueError("'availableAmount' not fund in response.")
        
        balance_key = self.balance.register_balance(agency_number=branchCode,
                                                    account_number=accountnumber,
                                                    balance_value=balance_value)

        self.requests.register_requests(
                request_type="GET", 
                balance_key=balance_key, 
                method="GET", 
                endpoint="balance", 
                payload={},
                status_code=status, 
                response=response_json)
        
        return response_json
    
    
    def get_account_extract(self, bankdoc:str, branchCode:str, accountnumber:str, start_date:str, end_date:str):
        bankaccount = f"{branchCode:04}.{accountnumber:07}"
        response_json, status = self.santander_bank_statement_connector.get_extract_account(bankdoc=bankdoc,
                                                                                            start_date=start_date,
                                                                                            end_date=end_date,
                                                                                            bankaccount=bankaccount)
        
        extract_key = self.extract.register_extract(branchCode=branchCode,
                                                    accountnumber=accountnumber,
                                                    start_date=start_date,
                                                    end_date=end_date)
        
        self.requests.register_requests(
            request_type="GET", 
            extract_key=extract_key,
            method="GET", 
            endpoint="extract", 
            payload={},
            status_code=status, 
            response=response_json)
        
        return response_json