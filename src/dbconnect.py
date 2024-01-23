import mariadb
import sys

class Database_Connection():
    def __init__(self, user, password, host, port, database, con, cur):
        self.user = user
        self.password = password
        self.host = host
        self.port = port 
        self.database = database
        self.con = con
        self.cur = cur

        con = mariadb.connect(
        user = "ole",
        password = "QrsoL82",
        host = "", 
        port = 3306,
        database = "BunnyDB"
        )
        
        
        cur = con.cursor()
        