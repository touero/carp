from abc import ABC
from unil import write_tolocal_mysql as wtm, log_t

from robot import Robot


class MeiShiTianXia_Robot(Robot, ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        return '美食天下'

    def run_task(self):
        home_cook_list = self.wait_elements_by_xpath('//h2')
        home_cook_img_list = []

        # 获取图片信息
        home_cook_imgs = self.find_elements_by_xpath('//div[@class="pic"]//img')
        for home_cook_img in home_cook_imgs:
            home_cook_img_list.append(home_cook_img.get_attribute('src'))

        # 获取用料
        home_cook_materials = self.find_elements_by_xpath('//ul/li/div[2]/p[2]')
        home_cook_materials_list = []
        for home_cook_material in home_cook_materials:
            home_cook_materials_list.append(home_cook_material.text)

        # 获取家常菜名字与链接信息
        home_cook_name_list = []
        home_cook_url_list = []
        for home_cook in home_cook_list:
            home_cook_name_list.append(home_cook.text)
            home_cook_url_list.append(home_cook.find_element('//h2/a').get_attribute('href'))

        # 制作家常菜字典
        for i in range(0, len(home_cook_name_list)):
            try:
                home_cook_dict = {'home_cook_name': home_cook_name_list[i], 'home_cook_img': home_cook_img_list[i],
                                  'home_cook_materials': home_cook_materials_list[i],
                                  'home_cook_url': home_cook_url_list[i]}
                wtm(home_cook_dict, 'mstx')
            except Exception as e:
                log_t(e)
