"""
SQLite3 DB API
"""
import sqlite3
from seldom.db_operation.base_db import SQLBase


class SQLiteDB(SQLBase):
    """SQLite3 DB table API"""

    def __init__(self, db_path: str):
        """
        Connect to the sqlite database
        """
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def close(self) -> None:
        """
        Close the database connection
        """
        self.connection.close()

    def execute_sql(self, sql: str) -> None:
        """
        Execute SQL
        """
        self.cursor.execute(sql)
        self.connection.commit()

    def insert_data(self, table: str, data: dict) -> None:
        """
        insert sql statement
        """
        for key in data:
            data[key] = "'" + str(data[key]) + "'"
        key = ','.join(data.keys())
        value = ','.join(data.values())
        sql = f"""insert into {table} ({key}) values ({value})"""
        self.execute_sql(sql)

    def query_sql(self, sql: str) -> list:
        """
        Query SQL
        return: query data
        """
        data_list = []
        rows = self.cursor.execute(sql)
        for row in rows:
            data_list.append(row)
        return data_list

    def select_data(self, table: str, where: dict = None) -> list:
        """
        select sql statement
        """
        sql = f"""select * from {table} """
        if where is not None:
            sql += f""" where {self.dict_to_str_and(where)};"""
        return self.query_sql(sql)

    def update_data(self, table: str, data: dict, where: dict) -> None:
        """
        update sql statement
        """
        sql = f"""update {table} set """
        sql += self.dict_to_str(data)
        if where:
            sql += f""" where {self.dict_to_str_and(where)};"""
        self.execute_sql(sql)

    def delete_data(self, table: str, where: dict = None) -> None:
        """
        delete table data
        """
        sql = f"""delete from {table}"""
        if where is not None:
            sql += f""" where {self.dict_to_str_and(where)};"""
        self.execute_sql(sql)

    def init_table(self, table_data: dict) -> None:
        """
        init table data
        """
        for table, data_list in table_data.items():
            self.delete_data(table)
            for data in data_list:
                self.insert_data(table, data)
