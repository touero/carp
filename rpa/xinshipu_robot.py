from abc import ABC
from unil import write_tolocal_mysql as wtm
from selenium.webdriver.support.wait import WebDriverWait, TimeoutException
from selenium.webdriver.common.by import By

from robot import Robot


class XinShiPu_Robot(Robot):
    def __init__(self, default_config, url):
        super().__init__(default_config, url)

    def run_task(self):
        dessert_list = self.find_eles_xpath('//img')
        # 获取甜品图片
        dessert_imgs = self.driver.find_elements(By.XPATH, '//div[@class="v-pw"]/img')
        # 用于最后字典生成时的标志，用来取出做法链接与甜点图片
        flag = 0
        dessert_img_list = []
        for dessert_img in dessert_imgs:
            dessert_img = dessert_img.get_attribute('src')
            dessert_img_list.append(dessert_img)
        # 获取甜品做法详细链接
        dessert_urls = self.driver.find_elements(By.XPATH, '//div[@class="bpannel cb"]/a')
        dessert_url_list = []
        for dessert_url in dessert_urls:
            dessert_url = dessert_url.get_attribute('href')
            dessert_url_list.append(dessert_url)
            print(dessert_url)

        for dessert in dessert_list:
            dessert.click()
            self.switch_last_window()
            # 获取甜品标题与用料
            dessert_name = self.get_ele_text('//h1')
            dessert_materials = self.driver.find_element(By.XPATH, '//div[@class="dd"]//p').text
            # 生成菜品字典，并用于写入数据库
            dessert_dict = {'dessert_name': dessert_name, 'dessert_img': dessert_img_list[flag], 'dessert_materials': dessert_materials, 'dessert_url': dessert_url_list[flag]}
            # print(dessert_dict)
            wtm(dessert_dict, 'xsp')
            flag = flag + 1
            self.close_window()
            self.switch_default_windows()