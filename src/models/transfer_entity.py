from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum, String
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
from enum import Enum as PyEnum
from models.db_base import Base
from models.connection import engine
from models.workspace_entity import Workspace

Session = sessionmaker(bind=engine)


class Payment(PyEnum):
    yes = "yes"
    no = "no"

class Transfer(Base):
    __tablename__ = "transfer"

    id = Column(Integer, primary_key=True)
    transfer_id = Column(String(36), nullable=False)
    workspace_id = Column(Integer, ForeignKey('workspace.id'), nullable=False) 
    value = Column(String, nullable=False) 
    confirm_payment = Column(Enum(Payment), nullable=False, default=Payment.no) 
    created_at = Column(DateTime, default=datetime.utcnow)

    workspace = relationship('Workspace', back_populates='transfers')
    requests = relationship("Requests", back_populates="transfer")

    def register_transfer(self, transfer_id, external_id, value):
        session = Session()
        try:
            result = session.query(Workspace.id).filter(Workspace.external_id == external_id).first()
            if result:
                workspace_id = result[0]
                transfer_data = Transfer(
                    transfer_id=transfer_id,
                    workspace_id=workspace_id,
                    value=value,
                )
                
                session.add(transfer_data)
                session.commit()
                
                print("Successfully registered transfer!")
                return transfer_data.id
            else:
                print("Workspace not found with the given external_id.")
                
        except Exception as e:
            print(f"Error registering transfer: {e}")
            session.rollback()
        finally:
            session.close()        
    
    def update_transfer(self, transfer_id):
        session = Session()
        try:
            transfer_record = session.query(Transfer).filter_by(transfer_id=transfer_id).one_or_none()

            if transfer_record:
                transfer_record.confirm_payment = Payment.yes
                session.commit()
            else:
                print(f"No transfers found for ID: {transfer_id}")

        except Exception as e:
            session.rollback()
            print(f"An error occurred while updating the transfer: {e}")
        finally:
            session.close()

    def __repr__(self):
        return f"Transfer: [id={self.id}, transfer_id={self.transfer_id}, workspace_id={self.workspace_id}, value={self.value}]"