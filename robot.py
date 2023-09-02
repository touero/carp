import pymysql
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from webdriverRe import WebDriverRe


class Robot(ABC, WebDriverRe):

    def __init__(self, **kwargs):
        super().__init__()
        self.task = kwargs.get('default_config')
        self.url = kwargs.get('url')
        self.task_type = kwargs.get('task_type')

        self.driver.get(self.url)
        self.driver.maximize_window()

    @abstractmethod
    def run_task(self):
        raise NotImplementedError


@dataclass
class DataBaseInfo:
    host: str
    user: str
    password: str
    database: str
    port: int = 3306


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

    def __del__(self):
        self.conn.close()
        self.cursor.close()
