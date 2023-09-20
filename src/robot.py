import pymysql
from abc import abstractmethod
from dataclasses import dataclass
from typing import Optional

from src.unil import log_t, send_email
from src.webdriver_re import WebDriverRe


class Robot(WebDriverRe):

    def __init__(self, **kwargs):
        super().__init__()
        self.need_save_list = []
        self.task = kwargs.get('default_config')
        self.url = kwargs.get('url')
        self.task_type = kwargs.get('task_type')
        self.task['url'] = self.url
        print(f'[start_url]: {self.url}')
        self.start_get(self.url)

    @abstractmethod
    def run_task(self):
        raise NotImplementedError

    def update_info_by_email(self, **kwargs):
        img = kwargs.get('img')
        msg = kwargs.get('msg')
        file = kwargs.get('file')
        if self.task.get('smtp_config'):
            log_t('[Update_info_by_email]')
            smtp_config = self.task['smtp_config']
            send_email(smtp_config, msg, img, file)
        else:
            log_t('email: False')


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
