from sqlalchemy import create_engine
from sqlmodel import SQLModel

engine=create_engine(
    url="sqlite:///sqlite.db",
    echo=True,
    #check_same_thread : desont allow to run fastapi and sqlengine on same thread
    connect_args={
        "check_same_thread":False,
    }
)

def create_db_tables():
    from .models import Shipment
    SQLModel.metadata.create_all(bind=engine)