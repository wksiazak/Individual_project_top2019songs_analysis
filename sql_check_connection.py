import pymysql

class ConnectionConfig:
    def connection(self, user="TOPsongs_project_user", passwd="qwerty1234"):
        self.conn = pymysql.connect("localhost", user, passwd, "TOPsongs_project")
        if (self.conn):
            print("...connected with database..")
        else:
            print("error")
        return self.conn

    def closeConnection(self):
        self.conn.close()
        print("...connection closed...")

c = ConnectionConfig()
c.connection(user="TOPsongs_project_user", passwd="qwerty1234")