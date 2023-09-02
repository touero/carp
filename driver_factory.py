from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions, Chrome

from setting import DRIVER_VERSION


class DriverFactory:
    def __init__(self):
        self.options = ChromeOptions()
        self.options.add_argument("disable-blink-features=AutomationControlled")
        self.options.add_experimental_option("excludeSwitches", ['enable-automation'])
        self.options.add_experimental_option('detach', True)

        self.service = Service(executable_path=f'./webdriver/chromedriver_windows_{DRIVER_VERSION}.exe')
        self.driver = Chrome(options=self.options, service=self.service)

