from unil import log_t, write_to_excel
from robot import Robot


class ShuGuoWang_Robot(Robot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        return '蔬果网'

    def run_task(self):
        price_list = self.wait_elements_by_xpath('//ul[@id="NongHuaZhuanYongFei1"]/li/a')
        for price in price_list:
            price.click()
            self.switch_last_window()
            self.get_xigua_xianggu()
            if self.find_ele_xpath('//a[text()="下一页"]'):
                self.find_ele_click_xpath('//a[text()="下一页"]')
                data = self.get_xigua_xianggu().split("\n")
                self.close_window()
                self.switch_last_window()
                self.need_save_list.append(data)
                log_t(data)
            else:
                self.close_window()
                self.switch_last_window()
        number = 1
        for i in range(0, 23):
            if number % 40 == 0:
                self.find_ele_click_xpath('//a[text()="下一页"]')
            price_list = self.find_elements_by_xpath(f'//ul[@id="NongHuaZhuanYongFei1"]//li[@tag="show_{i + 1}"]/a')
            number = 0
            for price in price_list:
                price.click()
                self.switch_last_window()
                self.get_xigua_xianggu()
                if self.find_ele_xpath('//a[text()="下一页"]'):
                    self.find_ele_click_xpath('//a[text()="下一页"]')
                    if self.get_xigua_xianggu():
                        data = self.get_xigua_xianggu().split("\n")
                        self.need_save_list.append(data)
                        log_t(data)
                        self.last_win()
                    else:
                        self.last_win()
                    number += 1
                else:
                    self.last_win()
                    number += 1
        write_to_excel(self.need_save_list, './output/guoshuwang_data.xlsx')

    def last_win(self):
        self.close_window()
        self.switch_last_window()

    def get_xigua_xianggu(self):
        rows = self.find_elements_by_xpath('//div[@class="pri_k"]/p')
        for row in rows:
            if '西瓜' in row.text:
                return row.text
