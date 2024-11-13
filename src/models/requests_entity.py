from sqlalchemy import Column, String, Integer, ForeignKey, JSON
from sqlalchemy.orm import sessionmaker, relationship
from models.db_base import Base
from models.connection import engine
from models.extracts_entity import Extracts
from models.balance_entity import Balance

Session = sessionmaker(bind=engine)

class Requests(Base):
    __tablename__ = "requests"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    request_type = Column(String, nullable=False)
    extract_key = Column(Integer, ForeignKey("extracts.id"), nullable=False)
    balance_key = Column(Integer, ForeignKey("balance.id"), nullable=False)
    transfer_key = Column(Integer, ForeignKey('transfer.id'))
    workspace_key = Column(Integer, ForeignKey('workspace.id'))
    method = Column(String(50), nullable=False)
    endpoint = Column(String(), nullable=False)
    payload = Column(JSON(), nullable=False)
    status_code = Column(Integer(), nullable=False)
    response = Column(JSON(), nullable=False)

    extract = relationship("Extracts", back_populates="requests")
    balance = relationship("Balance", backref="requests")
    transfer = relationship("Transfer", back_populates="requests")
    workspace = relationship("Workspace", back_populates="requests")

    def register_requests(self, request_type, method, endpoint, payload, status_code, response, transfer_key=None, extract_key=None, balance_key=None, workspace_key=None):
        session = Session()
        try:
            requests_data = Requests(
                request_type=request_type,
                transfer_key=transfer_key,
                extract_key=extract_key,
                balance_key=balance_key,
                workspace_key=workspace_key,
                method=method,
                endpoint=endpoint,
                payload=payload,
                status_code=status_code,
                response=response
            )
            session.add(requests_data)
            session.commit()
            print("Successfully registered request!")
            
        except Exception as e:
            print(f"Error registering request: {e}")
            session.rollback()
            
        finally:
            session.close()
            
    def __repr__(self):
        return (f"Requests: [id={self.id}, request_type={self.request_type}, transfer_key={self.transfer_key}, "
                f"extract_key={self.extract_key}, balance_key={self.balance_key}, method={self.method}, "
                f"endpoint={self.endpoint}, payload={self.payload}, status_code={self.status_code}, response={self.response}]")