import time

from .robot import Robot, log


class Railway_Robot(Robot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.info = self.task.get('12306_info', None)
        self.travel_list = []
        self.sale_time = ''

    def __str__(self):
        return '12306'

    def run_task(self):
        self.prepare()
        self.login()
        self.check_time()
        self.book()

    def prepare(self):
        config_values_list = list(self.info.values())
        if not all(config_values_list) and self.info is None:
            raise Exception('config缺少或不存在')

    def login(self):
        for count in range(1, 11):

            if not self.wait_ele_xpath_safe('//a[@login-type="personal"]'):
                if self.find_ele_xpath_safe('//*[@id="ERROR"]'):
                    self.wait_ele_click_xpath_safe('//a[@id="login_user"]')
                self.wait_ele_click_xpath_safe('//li[@class="login-hd-account"]')
                self.wait_ele_xpath_safe('//div[@class="login-panel"]//div[@class="login-box"]')
                self.wait_ele_xpath_safe('//img[@id="J-qrImg"]')
                login_qrcode = self.find_ele_screenshot('//div[@class="login-panel"]//div[@class="login-box"]', f'login_qrcode.png')
                self.update_info_by_email(img=login_qrcode)
                self.wait_ele_xpath_safe('//a[@login-type="personal"]', 180)
                log(f'等待扫码180s, 剩余等待次数: {count}')
            else:
                break

        try:
            if self.wait_ele_xpath_safe('//li[@class="nav-item nav-item-w1"]', timeout=60):
                log('登录成功')
        except TimeoutError as e:
            log(f'login timeout: {e}')
        except Exception as e:
            log(f'login false:{e}')

    def check_time(self):
        self.wait_click_xpath('//*[@id="J-xinxichaxun"]/a')
        self.wait_click_xpath('//*[@id="megamenu-9"]/div[1]/ul/li[5]/a')
        # todo 查询车票放票时间
        self.input_clear_xpath('//*[@id="sale_time_date"]')
        time.sleep(0.5)
        self.send_keys_by_xpath('//*[@id="sale_time_date"]', self.info['travel_date'])
        self.find_ele_click_xpath('//*[@id="saleText"]')
        self.send_keys_by_xpath('//*[@id="saleText"]', self.info['start_station'])
        self.find_ele_click_xpath('//*[@id="citem_0"]')
        check_time = ''
        self.wait_ele_xpath_safe('//*[@id="sale-time1"]/div[1]/ul/li')
        rows = self.find_elements_by_xpath('//*[@id="sale-time1"]/div[1]/ul/li')
        for row in rows:
            station = row.find_element('.//div[@class="sale-station-name"]').text
            if self.info['start_station'] + '站' in station:
                check_time = row.find_element('.//div[@class="sale-time"]').text.replace('起售', '')
                self.sale_time = check_time
        if not check_time:
            raise '查询起售日期的起售时间失败'

    def book(self):
        log('开始订票')
        self.find_ele_click_xpath('//li[@class="nav-item nav-item-w1"]')
        self.wait_ele_click_xpath_safe('//*[@id="fromStationText"]')
        self.send_keys_by_xpath('//*[@id="fromStationText"]', self.info['start_station'])
        self.find_ele_click_xpath('//*[@id="citem_0"]')
        self.send_keys_by_xpath('//*[@id="toStationText"]', self.info['to_station'])
        self.find_ele_click_xpath('//*[@id="citem_0"]')
        self.send_keys_by_xpath('//*[@id="train_date"]', self.info['travel_date'])
        self.click_to_last_window_xpath('//*[@id="search_one"]')
        # todo 检查起售时间才能继续
        # if self.find_ele_xpath_safe('//*[@id="no_filter_ticket_6"]/p'):
        #     log('出发日时间不允许')
        #     self.close_window()
        #     return
        rows = self.wait_elements_by_xpath('//tbody[@id="queryLeftTable"]/tr')
        for row in rows:
            if row.get_attribute('style') == 'display: none;':
                continue
            car_number = row.find_element('.//div/a').text
            start_station = row.find_element('./td[1]/div/div[2]/strong[1]').text
            to_station = row.find_element('./td[1]/div/div[2]/strong[2]').text
            start_time = row.find_element('./td[1]/div/div[3]/strong[1]').text
            to_time = row.find_element('./td[1]/div/div[3]/strong[2]').text
            is_have = row.find_element('./td[4]').text
            got_travel = {'car_number': car_number,
                          'start_station': start_station,
                          'to_station': to_station,
                          'start_time': start_time,
                          'to_time': to_time,
                          'is_have': is_have,
                          }
            print(got_travel)
            self.travel_list.append(got_travel)
            if start_station == self.info['start_station'] and to_station == self.info['to_station'] and \
                    start_time == self.info['start_time'] and to_time == self.info['to_time'] and is_have != '候补':
                # todo 此后的某个地方应该循环检测self.sale_time到放票时间点击购买之类
                row.find_element('.//td/a').click()
                if self.wait_ele_xpath_safe('//div[@id="content_defaultwarningAlert_hearder"]'):
                    hint = self.get_ele_text('//div[@id="content_defaultwarningAlert_hearder"]')
                    self.close_window()
                    raise Exception(hint)

                choices = self.wait_elements_by_xpath('//*[@id="normal_passenger_id"]/li', 10)
                for choice in choices:
                    person = choice.find_element('./label').text
                    if self.info['travel_person'] in person:
                        choice.find_element('./input').click()
                        break
                #  todo 请检查，可能出现乘车人不存在的情况目前想到any这一系列方法
                log('请检查，可能出现乘车人不存在的情况')
                self.find_ele_click_xpath('//a[text()="提交订单"]')
                site = f'//*[@id="erdeng1"]/ul/li/a[@id="1{self.info["seat"]}"]'
                self.wait_click_xpath(site)
                self.find_ele_click_xpath('//*[@id="qr_submit_id"]')
                if self.wait_ele_xpath_safe('//*[@id="orderResultInfo_id"]/p'):
                    hint = self.get_ele_text('//*[@id="orderResultInfo_id"]/p')
                    if '抱歉' in hint:
                        raise Exception(f'订票失败，{hint}')
                    else:
                        log('成功, 若当日已经购票且时间冲突,12306则会在查询页面显示为订票失败')
                break
