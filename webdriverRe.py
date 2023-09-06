import random
import time
from typing import List

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait, TimeoutException

from driver_factory import DriverFactory
from unil import log_t


class WebDriverRe:
    def __init__(self):
        self.driver = DriverFactory().driver

    def kill_driver(self):
        self.driver.quit()

    def wait_ele_click_xpath_safe(self, xpath: str, timeout: int = 5):
        try:
            WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located((By.XPATH, xpath)))
            self.driver.find_element(By.XPATH, xpath).click()
        except TimeoutException:
            log_t(f'Not waiting until: {xpath}')

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

    def find_ele_xpath_safe(self, xpath: str) -> bool:
        try:
            ele = self.driver.find_element(By.XPATH, xpath)
            if ele:
                return True
        except NoSuchElementException:
            log_t(f'Message: no such element: "method":"xpath","selector":"{xpath}"')
            return False

    def find_ele_xpath(self, xpath: str):
        return self.driver.find_element(By.XPATH, xpath)

    def close_window(self) -> None:
        self.driver.close()

    def wait_ele_by_xpath(self, xpath, timeout=5):
        WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located((By.XPATH, xpath)))

    def switch_default_windows(self):
        handle = self.driver.window_handles
        self.driver.switch_to.window(handle[0])

    def wait_find_by_xpath(self, xpath, timeout: int = 5) -> WebElement:
        WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located((By.XPATH, xpath)))
        return self.driver.find_element(By.XPATH, xpath)

    def wait_eles_by_xpath(self, xpath: str, timeout: int = 5) -> List[WebElement]:
        try:
            return WebDriverWait(self.driver, timeout).until(
                ec.presence_of_all_elements_located((By.XPATH, xpath)))
        except TimeoutException:
            return []

    def scroll_to_element_safe(self, ele: WebElement):
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

    def wait_frame_by_xpath(self, xpath: str, timeout: int = 5):
        WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located((By.XPATH, xpath)))
        self.driver.switch_to.frame(By.XPATH, xpath)

    def wait_frame_by_id(self, frame_id: str, timeout: int = 5):
        WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located((By.ID, frame_id)))
        self.driver.switch_to.frame(By.ID, frame_id)

    def switch_default_content(self):
        self.driver.switch_to.default_content()
