from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models.db_base import Base
from models.connection import engine


Session = sessionmaker(bind=engine)

class Balance(Base):
    __tablename__ = "balance"
    
    id = (Column(Integer, primary_key=True, autoincrement=True))
    agency_number = (Column(String, nullable=False))
    account_number = (Column(String, nullable=False))
    balance_value = (Column(String, nullable=False))
    created_at = Column(DateTime, default=datetime.utcnow)

    def register_balance(self, agency_number, account_number, balance_value):
        session = Session()
        try:
            balance_data = Balance(agency_number=agency_number,
                                account_number=account_number,
                                balance_value=balance_value)
            session.add(balance_data)
            session.commit()
            print("Successfully registered balance!")
            return balance_data.id
        
        except Exception as e:
            print(f"Error registering balance: {e}")
            session.rollback()
            
        finally:
            session.close()

    def __repr__(self):
        return f"Balance: [id={self.balance_value}, agency_number={self.agency_number}, account_number={self.account_number}]"
