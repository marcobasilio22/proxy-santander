import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
from models.tokens_entity import Tokens
from constants import (
    SANTANDER_TOKEN_CONSULT, 
    SANTANDER_TOKEN_TRANSFER,
    SANTANDER_ACCOUNT_SIGNED_CERTIFICATE,
    SANTANDER_CONSULT_CLIENT_ID,
    SANTANDER_CONSULT_CLIENT_SECRET,
    SANTANDER_TRANSFER_CLIENT_ID,
    SANTANDER_TRANSFER_CLIENT_SECRET
)


load_dotenv()


# Ao trocar o ambiente, as URLs serão as mesmas
class ValidationToken:
    def __init__(self):
        self.tokens = Tokens()
                
    def validation_consult_token(self):
        try:
            cert = SANTANDER_ACCOUNT_SIGNED_CERTIFICATE
            last_date = self.tokens.get_date('consult')
            
            if last_date is not None:
                last_date = last_date[0] 
                validate_time = datetime.utcnow()

                result = validate_time - last_date
                if result >= timedelta(minutes=15):
                    try:
                        token_url = SANTANDER_TOKEN_CONSULT
                        headers = {
                            "Content-Type": "application/x-www-form-urlencoded"
                        }
                        data = {
                            "client_id": SANTANDER_CONSULT_CLIENT_ID,
                            "client_secret": SANTANDER_CONSULT_CLIENT_SECRET,
                            "grant_type": "client_credentials"
                        }
                        
                        response = requests.post(token_url, headers=headers, cert=cert, data=data)
                        response.raise_for_status()
                        
                        token = response.json().get('access_token')
                        
                        if token:
                            self.tokens.update_token(1, token, 'consult') 
                        else:
                            raise ValueError("Token not found.")

                        if response.status_code == 200:
                            print("Request successful")
                        else:
                            print(f"Bad request: {response.status_code} - {response.text}")
                            
                    except Exception as e:
                        print(f"Error getting new token: {e}")
                        return None
                else:
                    print("Valid token. Within 15 minutes.")
                
                return last_date
            else:
                print("No date found.")
                return None
            
        except Exception as e:
            print(f"Error getting last token: {e}")
            return None  
        
    def validation_transfer_token(self):
        
        try:
            cert = SANTANDER_ACCOUNT_SIGNED_CERTIFICATE
            last_date = self.tokens.get_date('pix')
    
            if last_date is not None:
                last_date = last_date[0] 
                validate_time = datetime.utcnow()

                result = validate_time - last_date

                if result >= timedelta(minutes=15):
                    try:
                        token_url = SANTANDER_TOKEN_TRANSFER

                        headers = {
                            "Content-Type": "application/x-www-form-urlencoded"
                        }
                        data = {
                            "client_id": SANTANDER_TRANSFER_CLIENT_ID,
                            "client_secret": SANTANDER_TRANSFER_CLIENT_SECRET,
                            "grant_type": "client_credentials"
                        }
                        
                        response = requests.post(token_url, headers=headers, cert=cert, data=data)
                        response.raise_for_status()
                        
                        token = response.json().get('access_token')

                        if token:
                            self.tokens.update_token(2, token, 'pix') 
                        else:
                            raise ValueError("Token not found.")

                        if response.status_code == 200:
                            print("Request successful")
                        else:
                            print(f"Bad request: {response.status_code} - {response.text}")
                            
                    except Exception as e:
                        print(f"Error getting new token: {e}")
                        return None
                else:
                    print("Valid token. Within 15 minutes.")
                
                return last_date
            else:
                print("No date found.")
                return None
            
        except Exception as e:
            print(f"Error getting last token: {e}")
            return None  