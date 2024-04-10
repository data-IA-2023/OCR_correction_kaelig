from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, Date, select, update, delete, ForeignKeyConstraint
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
    commande = relationship("Commande", back_populates="fact")

    # Et les commandes ???

    def __str__(this):
        return f"FACTURE [{this.no}] {this.total}€"
    
class Commande(Base):
    __tablename__='commandes'
    facture_no = Column(String(255),ForeignKey("factures.no"),primary_key=True)
    produit_name = Column(String(255),ForeignKey("produits.name"),primary_key=True)
    no = Column(Integer)
    qty = Column(Integer)


    fact = relationship("Facture", back_populates="commande")
    produits = relationship("Produit", back_populates="comm")
    
class Produit(Base):
    __tablename__ = 'produits'
    name =  Column(String(255),primary_key=True)
    price = Column(Integer)
    comm = relationship("Commande", back_populates="produits")



Base.metadata.create_all(bind=engine)