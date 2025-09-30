'''from sqlalchemy import create_engine

engine = create_engine('sqlite:///:memory:')
connection = engine.connect()
print("Hello, SQLAlchemy!")
connection.close()
'''

import datetime
from sqlalchemy import *
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, joinedload
from dotenv import load_dotenv,dotenv_values

load_dotenv()

variaveis_de_ambiente = dotenv_values()
DATABASE_URL = variaveis_de_ambiente["DATABASE_URL"]


engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"  # O nome exato da tabela no banco de dados

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    senha_hash = Column(String(255), nullable=False)
    criado_em = Column(DateTime(timezone=True), default=datetime.datetime.now)

    notas = relationship("Nota", back_populates="autor")

class Nota(Base):
    __tablename__ = "notas"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    conteudo = Column(Text)
    titulo = Column(String(255), nullable=False)
    criado_em = Column(DateTime(timezone=True), default=datetime.datetime.now)
    modificado_em = Column(DateTime(timezone=True), default=datetime.datetime.now)

    autor = relationship("Usuario", back_populates="notas")


if __name__  == "__main__":
    Base.metadata.create_all(bind=engine)
    print("tabelas criadas com sucesso (se não existiam).")