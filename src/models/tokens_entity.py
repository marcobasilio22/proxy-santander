from sqlalchemy import Column, String, Integer, DateTime, Enum
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from enum import Enum as PyEnum
from models.db_base import Base
from models.connection import engine

Session = sessionmaker(bind=engine)
session = Session()
''
class TokenType(PyEnum):
    consult = "consult"
    pix = "pix"

class Tokens(Base):
    __tablename__ = "tokens"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String, nullable=False) 
    token_type = Column(Enum(TokenType), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def update_token(self, token_id, new_token, new_token_type): 
        try:
            token_to_update = session.query(Tokens).filter_by(id=token_id).first()
            
            if token_to_update:
                token_to_update.token = new_token
                token_to_update.token_type = new_token_type
                
                session.commit()
                
                print(f"Token updated successfully!")
            else:
                print(f"Token with id {token_id} not found.")
                
        except Exception as e:
            print(f"Error updating token: {e}")
            session.rollback()
        finally:
            session.close()

    def get_last_token(self, token_type):
        try:
            last_token = session.query(Tokens).filter(Tokens.token_type == token_type).order_by(Tokens.created_at.desc()).first()
            return last_token
        
        except Exception as e:
            print(f"Error getting last token: {e}")
            return None  
        
        finally:
            session.close()

    def get_date(self, token_type):
        try:
            last_date = session.query(Tokens.created_at).filter(Tokens.token_type == token_type).order_by(Tokens.created_at.desc()).first()
            return last_date
        
        except Exception as e:
            print(f"Error getting last token: {e}")
