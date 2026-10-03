import sqlite3

#make connection
connection=sqlite3.connect("sqlite.db")
#cursor to execute queries
cursor=connection.cursor()

#1.create table

cursor.execute("""
               CREATE TABLE IF NOT EXISTS shipment(
                   id INTEGER PRIMARY KEY,
                   content TEXT,
                   weight REAL,
                   status TEXT
               )
"""
)

#delete/ drop table
# cursor.execute("drop table shipment")
# connection.commit()

#2.add shipment data

# cursor.execute("""
#                INSERT INTO shipment VALUES(
#                    12701,
#                    'plam tress',
#                    15.23,
#                    'placed'
#                )
# """
# )

connection.commit()

#3.read shipment data

cursor.execute("""
select id,status from shipment
where content = 'plam tress'
"""
)
result = cursor.fetchall()
print(result)

#4. update shipment
# cursor.execute("""

# update shipment set status='in_transit' where id=12703
# """
# )
# connection.commit()

#5. update query parameters

status="placed"
id=12701

cursor.execute("""
update shipment set status = :status 
where id >:id
""",{"status":status,"id":id}
)
connection.commit()
#close connection
connection.close()

