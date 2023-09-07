from selenium.common.exceptions import TimeoutException
from unil import write_tolocal_mysql as wtm
from robot import Robot


class XiaChuFang_Robot(Robot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        return '下厨房'

    def run_task(self):
        food_list = self.wait_elements_by_xpath('//div[@class="info pure-u"]/p[@class="name"]/a')

        # 获取做法链接的url列表
        food_urls = self.find_elements_by_xpath('//div/p[1]/a')

        # 用于最后字典生成时的标志，用来取出做法链接
        food_urls_list = []
        flag = 0
        for food_url in food_urls:
            food_url = food_url.get_attribute('href')
            food_urls_list.append(food_url)

        # 点击进入菜品详情页面
        for food in food_list:
            food.click()
            self.switch_last_window()

            # 503页面出现，并解决
            try:
                self.wait_ele_by_xpath('//h1', 20)
            except TimeoutException:
                self.refresh()
                self.wait_ele_by_xpath('//h1', 20)

            # 获取食物名称
            food_name = self.get_ele_text('//h1')
            food_img = self.find_ele_xpath('//div[1]/img').get_attribute('src')

            # 获取用料列表并合并
            food_ma_list = []
            food_kg_list = []
            food_materials = []

            food_matril = self.find_elements_by_xpath('//table//tr/td[1]')
            for index, food_ma in enumerate(food_matril):
                if food_ma.text == '':
                    food_ma_list.append(self.get_ele_text(f'//table//tr[{index}]/td[1]/a'))
                else:
                    food_ma_list.append(food_ma.text)

            food_matril = self.find_elements_by_xpath('//table//tr/td[2]')
            for food_ma in food_matril:
                food_kg_list.append(food_ma.find_element('.////table//tr/td[2]').text)

            for i in range(0, len(food_ma_list)):
                food_materials.append(food_ma_list[i] + food_kg_list[i])

            # 生成菜品字典，并用于写入数据库
            food_dict = {'food_name': food_name, 'food_img': food_img, 'food_materials': ' '.join(food_materials),
                         'food_url': food_urls_list[flag]}
            wtm(food_dict, 'xcf')
            flag = flag + 1
            self.close_window()
            self.switch_default_windows()
