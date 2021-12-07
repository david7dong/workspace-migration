import mysql.connector
from mysql.connector import errorcode

class MySql:
    def __init__(self, host, user, password, database):
        try:
            self.cnx = mysql.connector.connect(user=user, password=password,
                                    host=host,
                                    database=database)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def query(self, query_str, params=None, alter=False):
        cursor = self.cnx.cursor()
        res = cursor.execute(query_str, params)
        if alter:
            self.cnx.commit()
        cursor.close()
        return res
