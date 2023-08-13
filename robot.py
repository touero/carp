import random
import time

import pymysql
import traceback
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait, TimeoutException

from constants import DEBUG
from unil import log_t


class Robot(ABC):

    def __init__(self, default_config, url):
        self.task = default_config
        self.url = url
        self.task_type = default_config['task_type']
        self.is_debug = self.task['is_debug']
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("disable-blink-features=AutomationControlled")
        self.options.add_experimental_option("excludeSwitches", ['enable-automation'])
        self.options.add_experimental_option('detach', True) if self.is_debug == DEBUG.IS.value else ...
        self.driver = webdriver.Chrome(options=self.options,
                                       executable_path='./webdriver/chromedriver_windows_114.exe')
        self.driver.get(self.url)
        self.driver.maximize_window()

    @abstractmethod
    def run_task(self):
        raise NotImplementedError

    def kill_robot(self):
        self.driver.quit()

    def wait_ele_click_xpath_safe(self, xpath: str, timeout: int = 5):
        try:
            WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located((By.XPATH, xpath)))
            self.driver.find_element(By.XPATH, xpath).click()
        except TimeoutException:
            ...

    def wait_ele_xpath_safe(self, xpath: str, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located((By.XPATH, xpath)))
            if self.driver.find_element(By.XPATH, xpath):
                return True
        except TimeoutException:
            return False

    def wait_click_xpath(self, xpath: str, timeout: int = 5):
        WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located((By.XPATH, xpath)))
        self.find_ele_click_xpath(xpath)

    def find_ele_click_xpath(self, xpath: str):
        self.driver.find_element(By.XPATH, xpath).click()

    def send_keys_xpath(self, xpath: str, keys: str):
        self.driver.find_element(By.XPATH, xpath).clear()
        self.driver.find_element(By.XPATH, xpath).send_keys(keys)

    def find_eles_xpath(self, xpath: str) -> list:
        if self.driver.find_elements(By.XPATH, xpath):
            return self.driver.find_elements(By.XPATH, xpath)
        return []

    def click_to_last_window_xpath(self, xpath: str):
        self.find_ele_click_xpath(xpath)
        handle = self.driver.window_handles
        self.driver.switch_to.window(handle[-1])

    def get_ele_text(self, xpath: str) -> str:
        text = None
        try:
            text = self.driver.find_element(By.XPATH, xpath).text
        except Exception as e:
            log_t(e)
        return text

    def input_clear_xpath(self, xpath: str):
        return self.driver.find_element(By.XPATH, xpath).clear()

    def switch_last_window(self):
        handle = self.driver.window_handles
        self.driver.switch_to.window(handle[-1])

    def refresh(self) -> None:
        self.driver.refresh()

    def find_ele_xpath(self, xpath: str) -> bool:
        try:
            ele = self.driver.find_element(By.XPATH, xpath)
            if ele:
                return True
        except Exception as e:
            log_t(e)
            return False

    def close_window(self) -> None:
        self.driver.close()

    def wait_ele_by_xpath(self, xpath, timeout=5):
        WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located((By.XPATH, xpath)))

    def switch_default_windows(self):
        handle = self.driver.window_handles
        self.driver.switch_to.window(handle[0])

    def wait_find_by_xpath(self, xpath, timeout=5) -> WebElement:
        WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located((By.XPATH, xpath)))
        return self.driver.find_element(By.XPATH, xpath)

    def wait_eles_by_xpath(self, xpath, timeout=10) -> List[WebElement]:
        try:
            return WebDriverWait(self.driver, timeout).until(
                ec.presence_of_all_elements_located((By.XPATH, xpath)))
        except TimeoutException:
            return []

    def scroll_to_element_safe(self, ele):
        self.execute_script(script="arguments[0].scrollIntoView(true)", ele=ele)

    def execute_script(self, **kwargs):
        try:
            script = kwargs.get('script')
            ele = kwargs.get('ele')
            ele = self.wait_ele_by_xpath(ele) if isinstance(ele, str) else ele
            self.driver.execute_script(script, ele)
        except Exception as e:
            log_t(e)

    def slide_to_right(self):
        if not self.wait_ele_xpath_safe('//*[@class="handler animate" and last() ]'):
            log_t('未发现滑块跳过')
            return
        for _ in range(3):
            try:
                if not self.wait_ele_xpath_safe('//*[@class="drag_text" and text()="验证通过"]'):
                    button = self.find_ele_xpath('//*[@class="handler animate" and last() ]')
                    ActionChains(self.driver).click_and_hold(button).perform()
                    ActionChains(self.driver).move_by_offset(random.randint(60, 100), 0).perform()
                    time.sleep(0.1)

                    ActionChains(self.driver).click_and_hold(button).perform()
                    ActionChains(self.driver).move_by_offset(random.randint(160, 200), 0).perform()
                    time.sleep(0.1)

                    ActionChains(self.driver).click_and_hold(button).perform()
                    ActionChains(self.driver).move_by_offset(360, 0).perform()
                    ActionChains(self.driver).release(button).perform()
                    time.sleep(1)
                else:
                    break
            except StaleElementReferenceException:
                self.find_ele_click_xpath('//*[@id="dom_id"]/div/span/a')


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
