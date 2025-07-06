# database Accounts
from dotenv import load_dotenv
import os
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

def conection_userprofile():
    host = os.getenv("DBU_HOSTIP")
    port = os.getenv("DBU_PORT")
    user = os.getenv("DBU_USER")
    password = urllib.parse.quote_plus(os.getenv("DBU_PASSWORD"))  # Escapa símbolos
    #password = os.getenv("DBU_PASSWORD")
    dbname = os.getenv("DBU_NAME")

    connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}"
    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    return Session()

