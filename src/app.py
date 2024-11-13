import falcon
import os
from dotenv import load_dotenv
from errors.api_error_handler import APIErrorHandler
from errors.base_error import QIException, error_verification
from middlewares.context_creator import ContextCreator
from middlewares.internal_authentication import InternalAuthenticationMiddleware
from resources.account_resource import AccountResource
from resources.transfer_resource import TransactionResource
from utils.logger import LogHandler
from wsgiref.simple_server import make_server

def create_app():
    
    load_dotenv()

    app = falcon.App(
        middleware=[
            ContextCreator(),
            InternalAuthenticationMiddleware()
        ]
    )

    account_resource = AccountResource()
    app.add_route("/santander_proxy/account", account_resource)
    app.add_route("/santander_proxy/account/balance/{bankdoc}/{branchCode}.{accountnumber}", account_resource, suffix="balance")
    app.add_route("/santander_proxy/account/extract/{bankdoc}/statements/{branchCode}.{accountnumber}", account_resource, suffix="extract")
    
    transaction_resource = TransactionResource()
    app.add_route("/santander_proxy/workspace", transaction_resource, suffix="workspace")
    app.add_route("/santander_proxy/payment", transaction_resource, suffix="payment")
    app.add_route("/santander_proxy/make_payment/{workspace_id}/{transfer_id}", transaction_resource, suffix="make_payment")
    
    return app

def main():
    error_verification()
    LogHandler()
    api = create_app()

    api.add_error_handler(Exception, APIErrorHandler.unexpected)
    api.add_error_handler(falcon.HTTPMethodNotAllowed, APIErrorHandler.method_not_allowed)
    api.add_error_handler(falcon.HTTPInvalidParam, APIErrorHandler.invalid_parameter)
    api.add_error_handler(QIException, APIErrorHandler.qi_exception)    
    return api

application = main()

if __name__ == "__main__":

    load_dotenv()

    host = os.getenv("HOST", "localhost")
    port = int(os.getenv("PORT", 3000))

    app = application

    with make_server(host, port, app) as httpd:
        print(f"Serviço rodando em http://{host}:{port}")
        httpd.serve_forever()