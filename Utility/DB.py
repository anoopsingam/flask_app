import mysql.connector
from Utility.Config import app_config


class Database:
    def __init__(self, table_name=None):
        """
        It connects to the database and creates a cursor object
        """
        try:
            if table_name is not None:
                self.table_name = table_name

            self.conn = mysql.connector.connect(host=app_config['DB_HOST'], user=app_config['DB_USER'],
                                                passwd=app_config['DB_PASSWORD'],
                                                database=app_config['DB_NAME'])
            self.exe = self.conn.cursor()
        except Exception as e:
            print(e)
            exit()

    def insert(self, table=None, data=None):
        """
        It takes a table name and a dictionary of key-value pairs and inserts the data into the table

        :param table: The table name
        :param data: a dictionary of the data you want to insert
        :return: The return value is a boolean value.
        """
        try:
            keys = []
            values = []
            for key, value in data.items():
                keys.append("`" + key + "`")
                values.append("'" + value + "'")
            keys = ",".join(keys)
            values = ",".join(values)
            if table is None:
                table = self.table_name
            self.exe.execute("INSERT INTO " + table + "({}) VALUES({}) ".format(keys, values))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def update(self, table=None, data=None, where=None):
        """
        It takes a table name, a dictionary of data to update, and a dictionary of where conditions. It
        then creates two lists, one for the data to update and one for the where conditions. It then
        joins the lists into strings and executes the query

        :param table: The table name
        :param data: The data you want to update
        :param where: This is the condition for the update
        :return: The return value is a boolean value.
        """
        try:
            sFinal, wFinal = [], []
            wkey, skey, wvalue, svalue = [], [], [], []
            for key, value in data.items():
                skey.append(key)
                svalue.append(value)
            for key, value in where.items():
                wkey.append(key)
                wvalue.append(value)
            for i in range(len(skey)):
                sFinal.append(skey[i] + "='" + svalue[i] + "'")
            for i in range(len(wkey)):
                wFinal.append(wkey[i] + "='" + wvalue[i] + "'")
            sFinal = ",".join(sFinal)
            wFinal = ",".join(wFinal)
            if table is None:
                table = self.table_name
            self.exe.execute(
                "UPDATE " + table + " SET {} WHERE {}".format(sFinal, wFinal))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def delete(self, table=None, where=None):
        """
        It deletes a row from a table in a database

        :param table: The table you want to delete from
        :param where: The data to be inserted into the table
        :return: The return value is a boolean value.
        """
        try:
            keys = []
            values = []
            for key, value in where.items():
                keys.append(key)
                values.append(value)
            keys = ",".join(keys)
            values = ",".join(values)
            if table is None:
                table = self.table_name

            self.exe.execute("DELETE FROM " + table +
                             " WHERE {}".format(keys, values))
            self.conn.commit()
        except Exception as e:
            print(e)
            return False

    def select(self, query):
        """
        It takes a query as a parameter, executes it, and returns the result as a list of dictionaries

        param query: The query to be executed
        :return: A list of dictionaries.
        """
        try:
            self.exe.execute(query)
            insertObject = []
            columnNames = [column[0] for column in self.exe.description]
            for record in self.exe.fetchall():
                insertObject.append(dict(zip(columnNames, record)))
            return insertObject
        except Exception as e:
            print(e)
            return False

    def check_value(self, table=None, where=None):
        """
        It checks if a value exists in a table

        :param table: The table you want to check
        :param where: The data to be inserted into the table
        :return: The return value is a boolean value.
        """
        try:
            wFinal = []
            wkey, wvalue = [], []
            for key, value in where.items():
                wkey.append(key)
                wvalue.append(value)
            for i in range(len(wkey)):
                wFinal.append(wkey[i] + "='" + wvalue[i] + "'")
            wFinal = " AND ".join(wFinal)

            if table is None:
                table = self.table_name
            self.exe.execute("SELECT * FROM " + table + " WHERE {}".format(wFinal))
            if self.exe.fetchone() is None:
                return False
            else:
                return True

        except Exception as e:
            print(e)
            return False

    def fetch(self, table=None, where=None):
        """
        It fetches a row from a table in a database

        :param table: The table you want to delete from
        :param where: The data to be inserted into the table
        :return: The return value is a boolean value.
        """
        try:

            if where is None:
                where = {"1": "1"}

            wFinal = []
            wkey, wvalue = [], []
            for key, value in where.items():
                wkey.append(key)
                wvalue.append(value)
            for i in range(len(wkey)):
                wFinal.append(wkey[i] + "='" + wvalue[i] + "'")
            wFinal = " AND ".join(wFinal)

            if table is None:
                table = self.table_name

            self.exe.execute("SELECT * FROM " + table + " WHERE {}".format(wFinal))
            insertObject = []
            columnNames = [column[0] for column in self.exe.description]
            for record in self.exe.fetchall():
                insertObject.append(dict(zip(columnNames, record)))
            return insertObject
        except Exception as e:
            print(e)
            return False

    def query(self, query):
        """
        It executes a query

        :param query: The query to be executed
        """
        return self.exe.execute(query)

    def fetchone(self, table=None, where=None):
        """
        It executes a query and returns the first row

        :param where:
        :param table:
        """
        try:

            keys = []
            values = []
            for key, value in where.items():
                keys.append(key)
                values.append(value)
            keys = ",".join(keys)
            values = ",".join(values)
            if table is None:
                table = self.table_name

            return self.exe.execute("SELECT * FROM " + table + " WHERE {}='{}'".format(keys, values)).fetchone()
        except Exception as e:
            print(e)
            return False
