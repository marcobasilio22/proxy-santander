from sqlalchemy import Column, Integer, Date
from sqlalchemy.orm import sessionmaker, relationship
from models.db_base import Base
from models.connection import engine


Session = sessionmaker(bind=engine)

class Extracts(Base):
    __tablename__ = "extracts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    agency_number = Column(Integer, nullable=False)
    account_number = Column(Integer, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    requests = relationship("Requests", back_populates="extract")
    
    def register_extract(self, branchCode, accountnumber, start_date, end_date):
        session = Session()
        try:
            extract_data = Extracts(agency_number=branchCode,
                                    account_number=accountnumber,
                                    start_date=start_date,
                                    end_date=end_date)
            session.add(extract_data)
            session.commit()
            print("Successfully registered extract!")
            return extract_data.id
        
        except Exception as e:
            print(f"Error registering extract: {e}")
            session.rollback()
            
        finally:
            session.close()
            
    def __repr__(self):
        return f"Extract: [id={self.id}, agency_number={self.agency_number}, account_number={self.account_number}, start_date={self.start_date}, end_date={self.end_date}]"
