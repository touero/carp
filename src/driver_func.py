from selenium.webdriver.common.alert import Alert
from selenium.webdriver.remote.webelement import WebElement as WebElement
from typing import List, Tuple, Optional
from abc import ABC, abstractmethod


class DriverFunc(ABC):
    driver: None
    @abstractmethod
    def __init__(self) -> None: ...

    @abstractmethod
    def start_get(self, url: str): ...

    @abstractmethod
    def driver_get(self, url): ...

    @abstractmethod
    def kill_driver(self) -> None: ...

    @abstractmethod
    def wait_ele_click_xpath_safe(self, xpath: str, timeout: int = ...): ...

    @abstractmethod
    def wait_ele_xpath_safe(self, xpath: str, timeout: int = ...) -> bool: ...

    @abstractmethod
    def wait_click_xpath(self, xpath: str, timeout: int = ...): ...

    @abstractmethod
    def find_ele_click_xpath(self, xpath: str): ...

    @abstractmethod
    def send_keys_by_xpath(self, xpath: str, keys: str): ...

    @abstractmethod
    def find_elements_by_xpath(self, xpath: str) -> list: ...

    @abstractmethod
    def click_to_last_window_xpath(self, xpath: str): ...

    @abstractmethod
    def get_ele_text(self, xpath: str) -> str: ...

    @abstractmethod
    def input_clear_xpath(self, xpath: str): ...

    @abstractmethod
    def switch_last_window(self) -> None: ...

    @abstractmethod
    def refresh(self) -> None: ...

    @abstractmethod
    def find_ele_xpath_safe(self, xpath: str) -> bool: ...

    @abstractmethod
    def find_ele_xpath(self, xpath: str): ...

    @abstractmethod
    def close_window(self) -> None: ...

    @abstractmethod
    def wait_ele_by_xpath(self, xpath, timeout: int = ...) -> None: ...

    @abstractmethod
    def switch_default_windows(self) -> None: ...

    @abstractmethod
    def wait_find_by_xpath(self, xpath, timeout: int = ...) -> WebElement: ...

    @abstractmethod
    def wait_elements_by_xpath(self, xpath: str, timeout: int = ...) -> List[WebElement]: ...

    @abstractmethod
    def scroll_to_element_safe(self, ele: WebElement): ...

    @abstractmethod
    def execute_script(self, **kwargs) -> None: ...

    @abstractmethod
    def slide_to_right(self) -> None: ...

    @abstractmethod
    def wait_frame_by_xpath(self, xpath: str, timeout: int = ..., must: bool = ...): ...

    @abstractmethod
    def wait_frame_by_id(self, frame_id: str, timeout: int = ..., must: bool = ...): ...

    @abstractmethod
    def switch_default_content(self) -> None: ...

    @abstractmethod
    def switch_default(self) -> None: ...

    @abstractmethod
    def wait_click_xpath_open_window(self, xpath: str, timeout: int = ...): ...

    @abstractmethod
    def get_attribute_by_xpath(self, xpath: str, attribute: str) -> str: ...

    @abstractmethod
    def wait_alert_handle(self, timeout: int = ..., must: bool = ..., accept: bool = ...): ...

    @abstractmethod
    def get_alert_text(self, timeout: int = ..., must: bool = ...) -> Tuple[Optional[Alert], str]: ...

    @abstractmethod
    def screenshot_full_png(self, name: str) -> str: ...

    @abstractmethod
    def find_ele_screenshot(self, xpath: str, name: str) -> str: ...

    @abstractmethod
    def wait_ele_disappear_by_xpath(self, xpath: str, timeout: int = ...): ...

