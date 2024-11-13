import falcon
from falcon import Request, Response
from controllers.transfer_controller import TransactionController

class TransactionResource:
    def on_post_workspace(self, req: Request, resp: Response):
        raw_body = req.media
        beneficiary = raw_body.get('mainDebitAccount', {})
        agency = beneficiary.get('branch')
        account = beneficiary.get('number')
        
        transaction_controller = TransactionController(req.context.instance)
        transaction = transaction_controller.post_workspace(agency=agency,
                                                            account=account)
        
        if isinstance(transaction, dict):  
            resp.media = transaction
        elif hasattr(transaction, 'to_dict'):
            resp.media = transaction.to_dict()
        else:
            resp.media = {
                "response": transaction.response_json,
            }
        
        resp.status = falcon.HTTP_200
        
    def on_post_payment(self, req: Request, resp: Response):
        raw_body = req.media
        beneficiary = raw_body.get('beneficiary', {})
        branchB = beneficiary.get('branch')
        numberB = beneficiary.get('number')
        typep = beneficiary.get('type')
        document_type = beneficiary.get('documentType')
        document_number = beneficiary.get('documentNumber')
        name = beneficiary.get('name')
        bank_code = beneficiary.get('bankCode')
        main_Debit_Account = raw_body.get('mainDebitAccount', {})
        branchD = main_Debit_Account.get("branch")
        numberD = main_Debit_Account.get("number")
        payment_value = raw_body.get('paymentValue')
        
        transaction_controller = TransactionController(req.context.instance)
        transaction = transaction_controller.post_payment(branchB=branchB,
                                                            numberB=numberB,
                                                            branchD=branchD,
                                                            numberD=numberD,
                                                            typep=typep,
                                                            document_type=document_type,
                                                            document_number=document_number,
                                                            name=name,
                                                            bank_code=bank_code,
                                                            payment_value=payment_value)
        
        if isinstance(transaction, dict):  
            resp.media = transaction
        elif hasattr(transaction, 'to_dict'):
            resp.media = transaction.to_dict()
        else:
            resp.media = {
                "Status" : "Payment was initiated and made successfully!",
                "response": transaction.response_json,
            }
        
        resp.status = falcon.HTTP_200
        
        
    def on_patch_make_payment(self, req: Request, resp: Response, workspace_id:str, transfer_id:str):
        raw_body = req.media
        payment_value = raw_body.get('paymentValue')
        
        transaction_controller = TransactionController(req.context.instance)
        transaction = transaction_controller.patch_make_payment(workspace_id=workspace_id,
                                                                transfer_id=transfer_id,
                                                                payment_value=payment_value)
        
        if isinstance(transaction, dict):  
            resp.media = transaction
        elif hasattr(transaction, 'to_dict'):
            resp.media = transaction.to_dict()
        else:
            resp.media = {
                "response": transaction.response_json,
            }
        
        resp.status = falcon.HTTP_200