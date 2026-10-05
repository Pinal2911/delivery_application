import sqlite3
from app.schemas import ShipmentCreate,ShipmentUpdate
from typing import Any
from contextlib import contextmanager

class Database:
    def connect_to_db(self):
        #make connection
        self.conn=sqlite3.connect("sqlite.db",check_same_thread=False)
        #cursor to execute queries
        self.cur=self.conn.cursor()

        
    def create_table(self):
        #create table
        self.cur.execute("""
                    CREATE TABLE IF NOT EXISTS shipment(
                        id INTEGER PRIMARY KEY,
                        content TEXT,
                        weight REAL,
                        status TEXT
                    )
        """
)

    def create(self,shipment:ShipmentCreate)->int:
        self.cur.execute("select max(id) from shipment")
        result=self.cur.fetchone()
        new_id=result[0]+1
        
        #insert value in table
        self.cur.execute("""
            insert into shipment
            values(:id,:content,:weight,:status)
        """,{
            "id": new_id,
            **shipment.model_dump(),
            "status":"placed",
        }
        )
        
        self.conn.commit()
        return new_id
    def get(self,id:int) -> dict[str,Any]| None:
        self.cur.execute("""
            select * from shipment
            where id=?
        """,(id,))
        
        row=self.cur.fetchone()
        return {
            "id":row[0],
            "content":row[1],
            "weight":row[2],
            "status":row[3]
        } if row else None
        
    def update(self,id:int,shipment:ShipmentUpdate) -> dict[str,Any]:
        self.cur.execute("""
        UPDATE shipment set status =:status
        where id = :id
        """,{
            "id":id,
            **shipment.model_dump()
        }
        )
        self.conn.commit()
        return self.get(id)
    
    def delete(self,id:int):
        self.cur.execute("""
        
        delete from shipment where id = ?
        """,(id,)
        )
        
        self.conn.commit()
        
    def close(self):
        print("...connection closed")
        self.conn.close()
        
@contextmanager
def managed_db():
    db=Database()
    print("enter setup...")
    db.connect_to_db()
    db.create_table()
    
    yield db
    
    print("exit the setup")
    db.close()
    

with managed_db() as db:
    print(db.get(12701))
    print(db.get(12703))
        
