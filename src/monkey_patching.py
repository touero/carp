from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
"""
    monkey_patching: Reducing operations for some selenium functions. 
    For example, set the default value:
    > elements: List[WebElement] = self.find_elements_by_xpath('//table/tr')
    > for element in elements:
    before:
        date = element.find_element(By.XPATH, './td[1]').text
    now:
        date = element.find_element('./td[1]').text
    
    ⚠️warning⚠️:
        There are some caveats to this approach, as monkey-patching may result in code that is harder to understand and 
    maintain, especially in larger projects. At the same time, when using monkey patches, be careful not to break the 
    behavior of the original class and ensure that your modifications do not introduce potential bugs
    
"""


def re_find_element(self, value, by=By.XPATH):
    return original_find_element(self, by, value)


original_find_element = WebElement.find_element
WebElement.find_element = re_find_element
