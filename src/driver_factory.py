from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions, Chrome
from DrissionPage import ChromiumPage

from src.setting import DRIVER_VERSION, DEBUG, DRISSION, CHROME_ADDRESS


class DriverFactory:
    def __init__(self):
        self.options = ChromeOptions()
        self.service = Service(executable_path=f'./webdriver/chromedriver_windows_{DRIVER_VERSION}.exe')
        if DRISSION:
            ChromiumPage(addr_driver_opts=CHROME_ADDRESS)
            self.options.add_experimental_option("debuggerAddress", CHROME_ADDRESS)
        else:
            self.options.add_argument("disable-blink-features=AutomationControlled")
            self.options.add_experimental_option("excludeSwitches", ['enable-automation'])
            self.options.add_experimental_option('detach', DEBUG)
            self.options.page_load_strategy = 'none'
            
        self.driver = Chrome(options=self.options, service=self.service)
