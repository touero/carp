import pymysql

from typing import Optional

from src.constants import DataBaseInfo


class SqlMaster:
    def __init__(self, db_info: Optional[DataBaseInfo] = None):
        self.conn = pymysql.connect(
            host=db_info.host,
            user=db_info.user,
            password=db_info.password,
            database=db_info.database,
            port=db_info.port
        )
        self.cursor = self.conn.cursor()

    def submit_sql_with_return(self, sql: str) -> tuple:
        """
        执行sql
        :param sql: sql语句
        :return: 元组，即有表的返回
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def only_submit_sql(self, sql: str):
        """
        执行sql
        :param sql: sql
        :return: None，即几行受影响
        """
        self.cursor.execute(sql)
        self.conn.commit()
