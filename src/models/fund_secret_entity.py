from models.db_base import Base
from sqlalchemy import Column, String, Integer


class FundSecret(Base):
    __tablename__ = "fund_secret"
    
    id = (Column(Integer, primary_key=True, autoincrement=True),)
    fund_number = (Column(Integer, nullable=False),)
    balance_service_key = (Column(String, nullable=False),)
    extract_service_key = (Column(String, nullable=False),)
    transfer_service_key = (Column(String, nullable=False),)

    def __repr__(self):
        return f"Fund secret: [id={self.id}, fund_number={self.fund_number}, balance_service_key={self.balance_service_key}, extract_service_key={self.extract_service_key}, transfer_service_key={self.transfer_service_key}]"
