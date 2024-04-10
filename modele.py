from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, Date, select, update, delete
from sqlalchemy.orm import relationship, sessionmaker, Session, mapped_column, declarative_base
from sqlalchemy import create_engine
import os, dotenv, requests, datetime, json, math, subprocess, re, glob, urllib, pyodbc

dotenv.load_dotenv()
BDD_URL=os.getenv('DATABASE_URL')
quoted_params = urllib.parse.quote_plus(BDD_URL)

conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(quoted_params)
# Connection à la BDD
engine = create_engine(conn_str, echo=True) # , echo=True
# classe de base dont no objets ORM vont dériver
Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'
    id  = Column(Integer, primary_key=True)
    name = Column(String)
    adr = Column(String)
    cat = Column(String)
    # 'factures' permet d'accéder aux factures (1..N) du clients
    factures = relationship("Facture", back_populates="client")

    def __str__(this):
        return f"CLIENT [{this.id}] {this.name} ({this.adr})"

class Facture(Base):
    __tablename__ = 'factures'
    no = Column(String(255), primary_key=True)
    dt = Column(DateTime)
    total = Column(Float)
    # client_id est la FK
    client_id = mapped_column(ForeignKey("clients.id"))
    # 'client' permet d'accéder au client lié à la facture
    client = relationship("Client", back_populates="factures")

    # Et les commandes ???

    def __str__(this):
        return f"FACTURE [{this.no}] {this.total}€"




Base.metadata.create_all(bind=engine)