from abc import abstractmethod, ABC
from typing import Optional

from src.tools import log, send_email
from .webdriver_re import WebDriverRe
from src.constants import SmtpInfo, DataBaseInfo
from src.sql_master import SqlMaster


class Robot(WebDriverRe, ABC):

    def __init__(self, **kwargs):
        super().__init__()
        self.smtp_info: Optional[SmtpInfo] = None
        self.need_save_list: list = []
        self.task: dict = kwargs.get('default_config')
        self.url: str = kwargs.get('url')
        self.task_type = kwargs.get('task_type')
        self.task['url'] = self.url
        print(f'[start_url]: {self.url}')
        self.start_get(self.url)
        if self.task.get('smtp_config'):
            self.smtp_info = SmtpInfo(self.task['smtp_config'])
        if self.task.get('is_mysql'):
            dbinfo = DataBaseInfo(self.task['dbinfo'])
            self.sql = SqlMaster(dbinfo)

    @abstractmethod
    def run_task(self):
        raise NotImplementedError

    def update_info_by_email(self, **kwargs):
        if self.smtp_info:
            img = kwargs.get('img')
            msg = kwargs.get('msg')
            file = kwargs.get('file')
            log('[Update_info_by_email]')
            send_email(self.smtp_info, msg, img, file)
        else:
            log('email: False')

    def task_finish(self):
        self.kill_driver()
        log('[kill driver success]')
