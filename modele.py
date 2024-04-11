from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, Date, select, update, delete, ForeignKeyConstraint
from sqlalchemy.orm import relationship, sessionmaker, Session, mapped_column, declarative_base
from sqlalchemy import create_engine
import os, dotenv, requests, datetime, json, math, subprocess, re, glob, urllib, pyodbc
from datetime import datetime

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

    def __str__(this):
        return f"no: [{this.no}] dt:{this.dt} total:({this.total} client_id:{this.client_id})"
    
    @staticmethod
    def read_file(no):
         with Session(engine) as session:
            query = select(Facture).where(Facture.no==no)
            res = session.execute(query).scalar()
            if not res:
                test=1000000
                test2=None
                test3=None
                ad,nom,cat,id=None,None,None,None
                with open(f"statics/{no}.png.txt",'r') as file:
                    prod={}
                    for i,line in enumerate(file):
                        if line.startswith('TOTAL'):
                            tot=line.split()
                            total=tot[1].replace('\n','')
                            total=total.replace(',','.')
                        if 'Euro' in line and 'TOTAL' not in line:
                            try :
                                prod[line.split('.',1)[0]]=[]
                                prqtt=line.split('.',1)[1]
                            except:
                                pass
                            else:
                                try:
                                    price=(prqtt.split('x',1)[1]).split()[0]
                                    prod[line.split('.',1)[0]].append(price)
                                    quantité=prqtt.split('x',1)[0]
                                    prod[line.split('.',1)[0]].append(quantité)
                                except:
                                    pass
                        if 'ddress' in line and not test2:
                            test=i
                            test2=1
                            ad=line.split()
                            ad=' '.join(ad[1:])
                        if test+1==i:
                            ad+=line
                        if 'Bill' in line and not test3: 
                            nom=' '.join(line.split()[2:])
                            test3=1
                                
                with open(f"statics/{no}.pngqr.txt",'r') as file:
                    for i,line in enumerate(file):
                        if line.startswith('DATE'):
                            date_mid=line.split(':',1)
                            date=datetime.strptime(date_mid[1].replace('\n',''), "%Y-%m-%d %H:%M:%S")
                        if line.startswith('CUST'):
                            id=line.split(':',1)[1].replace('\n','')
                            id=int(id)
                        if line.startswith('CAT'):
                            cat=line.split(':')[1]
                query = select(Client).where(Client.id==id)
                res1 = session.execute(query).scalar()
                if not res1:
                    client=Client(name=nom, adr=ad,cat=cat,id=id)
                    session.add(client)
                    session.commit()                    
                fac=Facture(no=no, total=total,dt=date,client_id=id)
                session.add(fac)
                session.commit()

                for key,value in prod.items():
                    query = select(Produit).where(Produit.name==key)
                    res2 = session.execute(query).scalar()
                    if not res2:
                        produit=Produit(name=key,price=value[0])
                        session.add(produit)
                        session.commit()

                for k,(key,value) in enumerate(prod.items()):
                    query = select(Commande).where((Commande.facture_no == no) & (Commande.produit_name == key))
                    res3 = session.execute(query).scalar()
                    if not res3:
                        quantity= re.findall(r'\d+',value[1])
                        quantity = ''.join(quantity)
                        comm=Commande(facture_no=no,produit_name=key,no=k+1,qty=int(quantity))
                        session.add(comm)
                        session.commit()

            else:
                fac=None
            return fac


    
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
    price = Column(Float)
    comm = relationship("Commande", back_populates="produits")

Base.metadata.create_all(bind=engine)



