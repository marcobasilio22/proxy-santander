import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()  

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_url = os.getenv('DATABASE_URL')

db_password_encoded = quote_plus(db_password)

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()

def close_connection():
    session.close()
    print("Database connection closed.")