"""Package imports"""
from sqlalchemy.orm import sessionmaker
from logger import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

def extract_data() -> dict:
    import requests

    func_name = 'get_data: '
    url = "https://dadosabertos.almg.gov.br/ws/proposicoes/pesquisa/direcionada?tp=1000&formato=json&ano=2023&ord=3"
    logger.info(func_name + 'Getting data from URL: ' + url)

    response = requests.get(url)
    if response.status_code != 200:
        logger.error(func_name + 'Error getting data from URL: ' + url)
        return {}
    else: 
        logger.info(func_name + 'Data successfully retrieved from URL: ' + url)
        data = response.json()
        return data

def clean_text(texto: str) -> str:
    cleaned_text = ' '.join(texto.split())
    return cleaned_text.replace('\n', '')

def transform_data(data: dict) -> list:
    from datetime import datetime

    func_name = 'clean_data: '

    cleaned_data = []

    logger.info(func_name + 'Starting to clean the data')
    for item in data['resultado']['listaItem']:
        try:
            proposicao = {
                'author': clean_text(item.get('autor', '').strip()),
                'presentationDate': datetime.strptime(item.get('dataPublicacao', ''), '%Y-%m-%d') if item.get('dataPublicacao', '') else None,
                'ementa': clean_text(item.get('ementa', '').strip()),
                'regime': item.get('regime', '').strip(),
                'situation': item.get('situacao', '').strip(),
                'propositionType': item.get('siglaTipoProjeto', '').strip(),
                'number': item.get('numero', '').strip(),
                'year': int(item.get('ano', 0)),
                'city': 'Belo Horizonte',
                'state': 'Minas Gerais'
            }
            cleaned_data.append(proposicao)

            tramitacoes = []
            for historico in item.get('listaHistoricoTramitacoes', []):
                tramitacao_data = {
                    'createdAt': datetime.strptime(historico.get('data', ''), '%Y-%m-%d') if historico.get('data', '') else None,
                    'description': clean_text(historico.get('historico', '').strip()),
                    'local': historico.get('local', '').strip()
                }
                tramitacoes.append(tramitacao_data)

            proposicao['tramitacoes'] = tramitacoes
            cleaned_data.append(proposicao)
        except Exception as e:
            logger.error(func_name + 'Error cleaning data: ' + str(e))
            continue

    return cleaned_data

def load_data(cleaned_data: list, session: sessionmaker) -> None:
    from src.db import Proposicao, Tramitacao
    from pandas import DataFrame

    func_name = 'load_data: '

    df = DataFrame(cleaned_data)
    df_unique = df.drop_duplicates(subset=['number'])

    logger.info(func_name + 'Starting to load data into the database')
    for proposicao_data in df_unique.to_dict(orient='records'):
        tramitacoes_data = proposicao_data.pop('tramitacoes', [])

        proposicao = Proposicao(**proposicao_data)

        for tramitacao_data in tramitacoes_data:
            tramitacao = Tramitacao(**tramitacao_data)
            proposicao.tramitacoes.append(tramitacao)

        try:
            session.merge(proposicao)
            session.commit() 
        except Exception as e:
            session.rollback()
            logger.error(f"{func_name}Error inserting proposition {proposicao.number}: {str(e)}")
            continue

        logger.info(f"{func_name}Proposition insertion completed successfully.")

    logger.info(f"{func_name}Data loading completed successfully.")

