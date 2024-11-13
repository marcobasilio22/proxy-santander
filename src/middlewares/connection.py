from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from constants import (
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_NAME,
    DATABASE_URL
)

db_user = DATABASE_USER
db_password = DATABASE_PASSWORD
db_host = DATABASE_HOST
db_port = DATABASE_PORT
db_name = DATABASE_NAME
db_url = DATABASE_URL

db_password_encoded = quote_plus(db_password)

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()

def close_connection():
    session.close()
    print("Database connection closed.")