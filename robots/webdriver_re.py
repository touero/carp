import random
import time
from abc import ABC
from typing import List, Optional, Tuple

from selenium.common import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait, TimeoutException

from src.driver_factory import DriverFactory
from src.setting import SCREENSHOT_DIR
from src.tools import log, get_time_now


class WebDriverRe(ABC):
    def __init__(self):
        self.driver = DriverFactory().driver
    
    def start_get(self, url: str):
        self.driver_get(url)
        self.driver.maximize_window()
    
    def driver_get(self, url: str):
        self.driver.get(url)

    def kill_driver(self):
        self.driver.quit()

    def wait_ele_click_xpath_safe(self, xpath: str, timeout: int = 5):
        try:
            WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located((By.XPATH, xpath)))
            self.driver.find_element(By.XPATH, xpath).click()
        except TimeoutException:
            log(f'Message: wait xpath timeout: "method":"xpath","selector":"{xpath}"')

    def wait_ele_xpath_safe(self, xpath: str, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located((By.XPATH, xpath)))
            if self.driver.find_element(By.XPATH, xpath):
                return True
        except TimeoutException:
            log(f'Message: wait xpath timeout: "method":"xpath","selector":"{xpath}"')
            return False

    def wait_click_xpath(self, xpath: str, timeout: int = 5):
        WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located((By.XPATH, xpath)))
        self.find_ele_click_xpath(xpath)

    def find_ele_click_xpath(self, xpath: str):
        self.driver.find_element(By.XPATH, xpath).click()

    def send_keys_by_xpath(self, xpath: str, keys: str):
        self.driver.find_element(By.XPATH, xpath).clear()
        self.driver.find_element(By.XPATH, xpath).send_keys(keys)

    def find_elements_by_xpath(self, xpath: str) -> List[WebElement]:
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
            log(e)
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
            log(f'Message: no such element: "method":"xpath","selector":"{xpath}"')
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

    def wait_elements_by_xpath(self, xpath: str, timeout: int = 5) -> List[WebElement]:
        try:
            return WebDriverWait(self.driver, timeout).until(ec.presence_of_all_elements_located((By.XPATH, xpath)))
        except TimeoutException:
            log(f'Message: wait xpath timeout: "method":"xpath","selector":"{xpath}"')
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
            log(e)

    def slide_to_right(self):
        if not self.wait_ele_xpath_safe('//*[@class="handler animate" and last() ]'):
            log('未发现滑块跳过')
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

    def wait_frame_by_xpath(self, xpath: str, timeout: int = 5, must: bool = False):
        try:
            WebDriverWait(self.driver, timeout).until(ec.frame_to_be_available_and_switch_to_it((By.XPATH, xpath)))
        except TimeoutException as e:
            log(f'Message: wait xpath timeout: "method":"xpath","selector":"{xpath}"')
            if must:
                raise e

    def wait_frame_by_id(self, frame_id: str, timeout: int = 5, must: bool = False):
        try:
            WebDriverWait(self.driver, timeout).until(ec.frame_to_be_available_and_switch_to_it((By.ID, frame_id)))
        except TimeoutException as e:
            log(f'Message: wait id timeout: "method":"xpath","selector":"{frame_id}"')
            if must:
                raise e

    def switch_default_content(self):
        self.driver.switch_to.default_content()

    def switch_default(self):
        self.switch_default_windows()
        self.switch_default_content()

    def wait_click_xpath_open_window(self, xpath: str, timeout: int = 5):
        before_handles = self.driver.window_handles
        self.wait_click_xpath(xpath, timeout)
        after_handles = self.driver.window_handles
        new_window = list(set(after_handles).difference(set(before_handles)))
        if not new_window:
            return
        self.driver.switch_to.window(new_window)

    def get_attribute_by_xpath(self, xpath: str, attribute: str) -> str:
        return self.find_ele_xpath(xpath).get_attribute(attribute)

    def wait_alert_handle(self, timeout: int = 5, must: bool = False, accept: bool = True):
        try:
            WebDriverWait(self.driver, timeout).until(ec.alert_is_present())
        except TimeoutException or NoAlertPresentException as e:
            log(f'Message: wait timeout: alert')
            if must:
                raise e
            else:
                return
        alert = self.driver.switch_to.alert
        log(alert.text)
        if accept:
            alert.accept()
        else:
            alert.dismiss()

    def get_alert_text(self, timeout: int = 5, must: bool = False) -> Tuple[Optional[Alert], str]:
        try:
            WebDriverWait(self.driver, timeout).until(ec.alert_is_present())
        except TimeoutException or NoAlertPresentException as e:
            log(f'Message: wait timeout: alert')
            if must:
                raise e
            else:
                return None, ''
        alert = self.driver.switch_to.alert
        return alert, alert.text

    def screenshot_full_png(self, name: str) -> str:
        now_time = get_time_now().strftime('%Y%m%d%H%M%S')
        path = f'{SCREENSHOT_DIR}{now_time}_{name}'
        self.driver.get_screenshot_as_file(path)
        return path

    def find_ele_screenshot(self, xpath: str, name: str) -> str:
        now_time = get_time_now().strftime('%Y%m%d%H%M%S')
        path = f'{SCREENSHOT_DIR}{now_time}_{name}'
        self.find_ele_xpath(xpath).screenshot(path)
        return path

    def wait_ele_disappear_by_xpath(self, xpath: str, timeout: int = 5):
        try:
            WebDriverWait(self.driver, timeout).until(ec.invisibility_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            log(f'Message: wait id timeout: "method":"xpath","selector":"{xpath}"')
