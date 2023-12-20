from src.exceptions import DriverVersionException
from src.setting import DETACH, HEADLESS, DRISSION, CHROME_ADDRESS
from src.constants import MachineType

from selenium.common import SessionNotCreatedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions, Chrome
from DrissionPage import ChromiumPage


class DriverFactory:
    def __init__(self):
        self.options = ChromeOptions()
        executable_path = MachineType.get_driver_path()
        self.service = Service(executable_path=executable_path)
        if DRISSION:
            ChromiumPage(addr_driver_opts=CHROME_ADDRESS)
            self.options.add_experimental_option("debuggerAddress", CHROME_ADDRESS)
        else:
            self.options.add_argument("disable-blink-features=AutomationControlled")
            self.options.add_argument('--headless') if HEADLESS else ...
            self.options.add_experimental_option("excludeSwitches", ['enable-automation'])
            self.options.add_experimental_option('detach', DETACH)
            self.options.page_load_strategy = 'none'
        try:
            self.driver = Chrome(options=self.options, service=self.service)
        except SessionNotCreatedException as e:
            if 'version of ChromeDriver only supports' in e.msg:
                raise DriverVersionException
