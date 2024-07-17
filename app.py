"""Package imports"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from os import getenv

"""Source imports"""
from src.db import *
from src.etl import *

load_dotenv()

if __name__ == '__main__':
    engine = create_engine(getenv('DATABASE_URL') or 'postgresql://postgres:password@localhost:5433/propositions_db')
    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(engine)

    raw_data = get_data()
    cleaned_data = clean_data(raw_data)
    load_data(cleaned_data, session)