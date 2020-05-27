import pymysql

class ConnectionConfig:
    def connection(self, user="TOPsongs_project_user", passwd="qwerty1234"):
        self.conn = pymysql.connect("localhost", user, passwd, "TOPsongs_project")
        if (self.conn):
            print("...połączono z bazą danych...")
        else:
            print("błąd połączenia")
        return self.conn

    def closeConnection(self):
        self.conn.close()
        print("...połączenie zakmniete...")