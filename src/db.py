"""Package imports"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Proposicao(Base):
    __tablename__ = 'proposicoes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    author = Column(String)
    presentationDate = Column(DateTime)
    ementa = Column(String)
    regime = Column(String)
    situation = Column(String)
    propositionType = Column(String)
    number = Column(String, unique=True) # Para evitar duplicatas
    year = Column(Integer)
    city = Column(String)
    state = Column(String)

    tramitacoes = relationship("Tramitacao", back_populates="proposicao")

class Tramitacao(Base):
    __tablename__ = 'tramitacoes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    propositionId = Column(Integer, ForeignKey('proposicoes.id'))
    createdAt = Column(DateTime)
    local = Column(String)
    description = Column(String)

    proposicao = relationship("Proposicao", back_populates="tramitacoes")