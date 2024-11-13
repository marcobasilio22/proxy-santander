import falcon
from falcon import Request, Response
from connectors.rest_connector import (
    BaseConnectorResponse
)
from controllers.account_controller import AccountController

class AccountResource:
    def on_get_balance(self, req: Request, resp: Response, bankdoc: str, branchCode: str, accountnumber: str):
        account_controller = AccountController(req.context.instance)
                
        balance_response = account_controller.get_account_balance(bankdoc=bankdoc,
                                                                    branchCode=branchCode,
                                                                    accountnumber=accountnumber)
        resp.media = balance_response
        resp.status = falcon.HTTP_200
                
        
    def on_get_extract(self, req: Request, resp: Response, bankdoc:str, branchCode:str, accountnumber:str):
        start_date = req.get_param_as_date('initialDate', required=True)
        end_date = req.get_param_as_date('finalDate', required=True)
        
        if not start_date or not end_date:
            resp.media = {"error": "The 'initialDate' and 'finalDate' parameters are mandatory"}
            resp.status = falcon.HTTP_400
            return

        account_controller = AccountController(req.context.instance)
        extract_data = account_controller.get_account_extract(bankdoc=bankdoc,
                                                                branchCode=branchCode,
                                                                accountnumber=accountnumber,
                                                                start_date=start_date, 
                                                                end_date=end_date)
        
        if isinstance(extract_data, BaseConnectorResponse):
            extract_data = extract_data.response_json 
        
        resp.media = extract_data
        resp.status = falcon.HTTP_200