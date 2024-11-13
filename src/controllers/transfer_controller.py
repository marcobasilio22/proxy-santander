from controllers.base_controller import BaseController
from utils.context import Context
from connectors.santander_transfer_connector import SantanderBankConnector
from models.workspace_entity import Workspace
from models.transfer_entity import Transfer
from models.requests_entity import Requests

class TransactionController(BaseController):
    def __init__(self, context: Context) -> None:
        super().__init__(context, __name__)
        self.workspace = Workspace()
        self.transfer = Transfer()
        self.requests = Requests()
        self.santander_bank_statement_connector = SantanderBankConnector(context)
                
    def post_workspace(self, agency, account):
        response_json, status = self.santander_bank_statement_connector.post_workspace(agency=agency,
                                                                                        account=account)
    
        workspace_id = response_json.get('id')
        
        workspace_key = self.workspace.register_workspace(external_id=workspace_id, 
                                                            account=account,
                                                            agency=agency)

        self.requests.register_requests(request_type="POST",
                                workspace_key=workspace_key,
                                method="POST",
                                endpoint="workspace",
                                payload=response_json,
                                status_code=status,
                                response=response_json)
        
        if not workspace_id:
            raise ValueError("O ID do workspace não foi retornado na resposta.")
        
        return response_json
    
    def post_payment(self, branchB, numberB, branchD, numberD, typep, document_type, document_number, name,  bank_code, payment_value):        
        workspace = Workspace()
        consult_workspace = workspace.find_workspace(numberD=numberD,
                                                    branchD=branchD)
        
        if consult_workspace is None:
            workspace_response_json, status_code = self.santander_bank_statement_connector.post_workspace(branchD=branchD,
                                                                                                            numberD=numberD)
            
            workspace_id = workspace_response_json.get('id')
            
            if workspace_id is None:
                raise ValueError("O ID do workspace não foi retornado na resposta.")
                
            workspace_key = self.workspace.register_workspace(external_id=workspace_id, 
                                                                account=numberD,
                                                                agency=branchD)
            
            self.requests.register_requests(
                request_type="POST",
                workspace_key=workspace_key,
                method="POST",
                endpoint="workspace",
                payload=workspace_response_json,
                status_code=status_code,
                response=workspace_response_json)

        elif consult_workspace is not None:
            workspace_id = consult_workspace

        payment_response_json, status_code = self.santander_bank_statement_connector.post_payment(workspace_id=workspace_id,
                                                                                                    branchB=branchB,
                                                                                                    numberB=numberB,
                                                                                                    typep=typep,
                                                                                                    document_type=document_type,
                                                                                                    document_number=document_number,
                                                                                                    name=name,
                                                                                                    bank_code=bank_code,
                                                                                                    payment_value=payment_value)
    
        transfer_id = payment_response_json.get('id')
        
        transfer_key = self.transfer.register_transfer(transfer_id=transfer_id,
                                                        external_id=workspace_id,
                                                        value=payment_value)
                        
        self.requests.register_requests(request_type="POST",
                                        transfer_key=transfer_key,
                                        method="POST",
                                        endpoint="payment",
                                        payload=payment_response_json,
                                        status_code=status_code, 
                                        response=payment_response_json)
        
        make_payment_response_json, status_code = self.santander_bank_statement_connector.patch_make_payment(workspace_id=workspace_id,
                                                                                                            transfer_id=transfer_id,
                                                                                                            payment_value=payment_value)
        
        self.transfer.update_transfer(transfer_id=transfer_id)
        
        self.requests.register_requests(request_type="PATCH",
                                method="PATCH",
                                endpoint='confirm_payment',
                                payload=make_payment_response_json,
                                status_code=status_code,
                                response=make_payment_response_json)

        return make_payment_response_json
    
    def patch_make_payment(self, workspace_id, transfer_id, payment_value):
        response_json, status = self.santander_bank_statement_connector.patch_make_payment(workspace_id=workspace_id,
                                                                                            transfer_id=transfer_id,
                                                                                            payment_value=payment_value)
        
        self.requests.register_requests(request_type="PATCH",
                                        method="PATCH",
                                        endpoint='confirm_payment',
                                        payload=response_json,
                                        status_code=status,
                                        response=response_json)
        return response_json