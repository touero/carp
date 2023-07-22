from abc import ABC
from unil import *
import unil
from robot import Robot


class ShuGuoWang_Robot(Robot):
    def __init__(self, default_config, url):
        super().__init__(default_config, url)

    def run_task(self):
        price_list = self.find_eles_xpath('//ul[@id="NongHuaZhuanYongFei1"]/li/a')
        for price in price_list:
            price.click()
            self.switch_last_window()
            self.get_xigua_xianggu()
            if self.find_ele_xpath('//a[text()="下一页"]'):
                self.find_ele_click_xpath('//a[text()="下一页"]')
                data = self.get_xigua_xianggu().split("\n")
                self.close_window()
                self.switch_last_window()
                write_to_excel(data, './output/guoshuwang_data.xlsx')
                print(data)
            else:
                self.close_window()
                self.switch_last_window()
        number = 1
        for i in range(0, 23):
            if number % 40 == 0:
                self.find_ele_click_xpath('//a[text()="下一页"]')
            price_list = self.find_eles_xpath(f'//ul[@id="NongHuaZhuanYongFei1"]//li[@tag="show_{i + 1}"]/a')
            number = 0
            for price in price_list:
                price.click()
                self.switch_last_window()
                self.get_xigua_xianggu()
                if self.find_ele_xpath('//a[text()="下一页"]'):
                    self.find_ele_click_xpath('//a[text()="下一页"]')
                    if self.get_xigua_xianggu():
                        data = self.get_xigua_xianggu().split("\n")
                        unil.write_to_excel(data, './output/guoshuwang_data.xlsx')
                        unil.log_t(data)
                        self.last_win()
                    else:
                        self.last_win()
                    number += 1
                else:
                    self.last_win()
                    number += 1

    def last_win(self):
        self.close_window()
        self.switch_last_window()

    def get_xigua_xianggu(self):
        rows = self.find_eles_xpath('//div[@class="pri_k"]/p')
        for row in rows:
            if '西瓜' in row.text:
                return row.text
