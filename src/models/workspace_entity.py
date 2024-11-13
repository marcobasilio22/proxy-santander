from sqlalchemy import Column, Integer, DateTime, and_
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
from models.db_base import Base
from models.connection import engine

Session = sessionmaker(bind=engine)

class Workspace(Base):
    __tablename__ = "workspace"

    id = Column(Integer, primary_key=True)
    external_id = Column(Integer, nullable=False)
    account = Column(Integer, nullable=False, unique=True) 
    agency = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    transfers = relationship('Transfer', back_populates='workspace')
    requests = relationship("Requests", back_populates="workspace")

    def register_workspace(self, external_id, account, agency):
        session = Session()
        try:
            if self.exists_workspace(external_id, account, agency):
                print("Registration already exists with this external_id, account and agency. Skipping insertion.")
                return 
            
            workspace_data = Workspace(external_id=external_id,
                                        account=account,
                                        agency=agency)
            
            session.add(workspace_data)
            session.commit()
            
            print("Successfully registered workspace!")
            
            return workspace_data.id
        
        except Exception as e:
            print(f"Error registering workspace: {e}")
            session.rollback()
        finally:
            session.close()

    def exists_workspace(self, external_id, account, agency):
        session = Session() 
        try:
            return session.query(Workspace).filter(
                and_(
                    Workspace.external_id == external_id,
                    Workspace.account == account,
                    Workspace.agency == agency
                )
            ).first() is not None
            
        except Exception as e:
            print(f"Error when checking the existence of the workspace: {e}")
            return False
        finally:
            session.close() 
            
    def find_workspace(self, numberD, branchD):
        session = Session()
        try:
            result = session.query(Workspace.external_id).filter(
                Workspace.account == numberD,
                Workspace.agency == branchD
            ).first()

            if result:
                return result.external_id
            else:
                print("No workspaces found for the provided account and agency.")
                return None
            
        except Exception as e:
            print(f"Error when searching for workspace: {e}")
            return None
        finally:
            session.close()

    def __repr__(self):
        return f"Workspace: [id={self.id}, external_id={self.external_id}, account={self.account}, agency={self.agency}]"