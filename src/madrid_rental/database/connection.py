from sqlalchemy import create_engine
from madrid_rental.config import DATABASE_URL

def get_engine():
    return create_engine(DATABASE_URL)
