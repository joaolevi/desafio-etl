"""Package imports"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import time
import logging

"""Source imports"""
from src.db import *
from src.etl import *


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    func_name = '__main__: '

    time.sleep(10)

    engine = create_engine(os.getenv('DATABASE_URL') or 'postgresql+psycopg2://postgres:password@db:5432/propositions_db')
    Session = sessionmaker(bind=engine)
    session = Session()
    if session is None:
        logger.error(func_name + 'Error connecting to database')
        exit(1)

    Base.metadata.create_all(engine)

    logger.info(func_name + 'Starting ETL process')
    raw_data = get_data()
    cleaned_data = clean_data(raw_data)
    load_data(cleaned_data, session)

    logger.info(func_name + 'ETL process finished')