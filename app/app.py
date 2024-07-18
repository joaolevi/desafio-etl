"""Package imports"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import time
import logging
from flask import Flask, request, jsonify, abort

"""Source imports"""
from src.db import *
from src.etl import extract_data, transform_data, load_data

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/etl', methods=['POST'])
def start_etl():
    logger.info('Starting ETL process')
    raw_data = extract_data()
    cleaned_data = transform_data(raw_data)
    load_data(cleaned_data, session)
    logger.info('ETL process finished')
    return jsonify({'message': 'ETL process finished'}, 200)

if __name__ == '__main__':
    time.sleep(10) # Waiting for DB to be ready

    engine = create_engine(os.getenv('DATABASE_URL') or 'postgresql+psycopg2://postgres:password@db:5432/propositions_db')
    Session = sessionmaker(bind=engine)
    session = Session()
    if session is None:
        logger.error('Error connecting to the database')
        exit(1)
    Base.metadata.create_all(engine)

    app.run(host='0.0.0.0', port=5000)
