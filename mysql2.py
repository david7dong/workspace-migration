import pymysql as MySQLdb

class MySql:
    def __init__(self, host, user, password, database):

        self.cnx = MySQLdb.connect(host=host, user=user, passwd=password, db=database)

    def query(self, query_str, params=[], alter=False):
        cursor = self.cnx.cursor()
        # execute SQL query using execute() method.
        cursor.execute(query_str, params)

        # Fetch a single row using fetchone() method.
        data = cursor.fetchall()
        if alter:
            self.cnx.commit()
        return data

    def execute_many(self, query_str, params, alter=True):
        cursor = self.cnx.cursor()
        cursor.executemany(query_str, params)
        if alter:
            self.cnx.commit()
