from abc import ABC
from unil import write_tolocal_mysql as wtm
from selenium.webdriver.support.wait import TimeoutException
from selenium.webdriver.common.by import By

from robot import Robot


class MeiShiTianXia_Robot(Robot, ABC):
    def __init__(self, default_config, url):
        super().__init__(default_config, url)

    def run_task(self):
        home_cook_list = self.find_eles_xpath('//h2')
        home_cook_img_list = []
        flag = 0
        # 获取图片信息
        home_cook_imgs = self.find_eles_xpath('//div[@class="pic"]//img')
        for home_cook_img in home_cook_imgs:
            home_cook_img_list.append(home_cook_img.get_attribute('src'))
        # 获取用料
        home_cook_materials = self.find_eles_xpath('//ul/li/div[2]/p[2]')
        home_cook_materials_list = []
        for home_cook_material in home_cook_materials:
            home_cook_materials_list.append(home_cook_material.text)

        # 获取家常菜名字与链接信息
        home_cook_name_list = []
        home_cook_url_list = []
        for home_cook in home_cook_list:
            home_cook_name_list.append(home_cook.text)
            home_cook_url_list.append(home_cook.find_element(By.XPATH, '//h2/a').get_attribute('href'))

        # 制作家常菜字典
        for i in range(0, len(home_cook_name_list)):
            try:
                home_cook_dict = {'home_cook_name': home_cook_name_list[i], 'home_cook_img': home_cook_img_list[i],
                                  'home_cook_materials': home_cook_materials_list[i],
                                  'home_cook_url': home_cook_url_list[i]}
                wtm(home_cook_dict, 'mstx')
            except:
                print("数据丢失")
            # print(home_cook_dict)

            # print(home_cook)
