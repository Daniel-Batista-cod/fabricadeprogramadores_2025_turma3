import datetime
from sqlalchemy import *
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, joinedload
from dotenv import load_dotenv, dotenv_values
import os
 
"""load_dotenv()
variaveis_de_ambiente = dotenv_values()
DATABASE_URL = variaveis_de_ambiente["DATABASE_URL"]

"""
DATABASE_URL= os.environ.get["DATABASE_URL"]

engine = create_engine(DATABASE_URL)

# a sessão é a nossa "area de trabalho" para conversar com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

usuario_endereco_associacao = Table(
    "usuario_endereco_associacao",
    Base.metadata,
    Column("usuario_id", Integer, ForeignKey("usuarios.id"), primary_key=True),
    Column("endereco_id", Integer, ForeignKey("enderecos.id"), primary_key=True),
)

usuario_curso_associacao = Table(
    "usuario_curso_associacao",
    Base.metadata,
    Column("usuario_id", Integer, ForeignKey("usuarios.id"), primary_key=True),
    Column("curso_id", Integer, ForeignKey("cursos.id"), primary_key=True),
)


class Usuario(Base):

    __tablename__ = "usuarios" 

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    senha_hash = Column(String(255), nullable=False)
    criado_em = Column(DateTime(timezone=True), default=datetime.datetime.now)

    notas = relationship("Nota", back_populates="autor")
    usuario_enderecos = relationship("Enderecos",
        secondary=usuario_endereco_associacao,
        back_populates="moradores"
        )
    
    usuario_cursos = relationship("Cursos",
        secondary=usuario_curso_associacao,
        back_populates="alunos")


class Nota(Base):
    __tablename__ = "notas"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    titulo = Column(String(255), nullable=False)
    conteudo = Column(Text)
    criado_em = Column(DateTime(timezone=True), default=datetime.datetime.now)
    modificado_em = Column(DateTime(timezone=True), default=datetime.datetime.now)

    #relacionamento inverso para o usuario
    autor = relationship("Usuario", back_populates="notas")


class Enderecos(Base):
    __tablename__ = "enderecos"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
   
    rua = Column(String(255), nullable=False)
    numero = Column(Integer)
    cep= Column(Integer)
    
    moradores = relationship(
        "Usuario", 
        secondary=usuario_endereco_associacao,
        back_populates="usuario_enderecos")
    

class Cursos(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(Text)

    alunos = relationship(
        "Usuario",
        secondary=usuario_curso_associacao,
        back_populates="usuario_cursos"
    )



if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso (Se não existiam).")

else:
    print("Erro")


