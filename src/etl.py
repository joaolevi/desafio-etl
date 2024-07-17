"""Package imports"""
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

def get_data() -> dict:
    import requests

    url = "https://dadosabertos.almg.gov.br/ws/proposicoes/pesquisa/direcionada?tp=1000&formato=json&ano=2023&ord=3"
    response = requests.get(url)
    data = response.json()
    return data

def clean_text(texto: str) -> str:
    cleaned_text = ' '.join(texto.split())
    return cleaned_text.replace('\n', '')

def clean_data(data: dict) -> list:
    from datetime import datetime

    cleaned_data = []
    contador = 1 # remover tbm
    for item in data['resultado']['listaItem']:
        contador += 1
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

        # somente teste - remover
        if contador == 10:
            break
    return cleaned_data

def load_data(cleaned_data: list, session: sessionmaker) -> None:
    from src.db import Proposicao, Tramitacao
    from pandas import DataFrame

    df = DataFrame(cleaned_data)

    df_unique = df.drop_duplicates(subset=['number'])

    for proposicao_data in df_unique.to_dict(orient='records'):
        tramitacoes_data = proposicao_data.pop('tramitacoes', [])

        proposicao = Proposicao(**proposicao_data)

        for tramitacao_data in tramitacoes_data:
            tramitacao = Tramitacao(**tramitacao_data)
            proposicao.tramitacoes.append(tramitacao)

        session.add(proposicao)

    session.commit()

