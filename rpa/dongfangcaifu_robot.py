from selenium.webdriver.common.by import By

from robot import Robot
from unil import *


class DongFangCaiFu_Robot(Robot):
    def __init__(self, default_config, url):
        super().__init__(default_config, url)

    def run_task(self):
        rows = self.wait_eles_by_xpath('//div[@id="table_ls"]//tbody//tr')
        for index, row in enumerate(rows):
            self.scroll_to_element_safe(row)
            log_t(f'第{index + 1}行')
            date = row.find_element(By.XPATH, './td[1]').text
            closing_price = row.find_element(By.XPATH, './td[2]').text
            fluctuation_range = row.find_element(By.XPATH, './td[3]').text
            main_net_inflow_net_amount = row.find_element(By.XPATH, './td[4]').text
            main_net_inflow_net_proportion = row.find_element(By.XPATH, './td[5]').text
            great_large_single_net_inflow_amount = row.find_element(By.XPATH, './td[6]').text
            great_large_single_net_inflow_proportion = row.find_element(By.XPATH, './td[7]').text
            large_order_net_inflow_amount = row.find_element(By.XPATH, './td[8]').text
            large_order_net_inflow_proportion = row.find_element(By.XPATH, './td[9]').text
            net_inflow_of_intermediate_orders_amount = row.find_element(By.XPATH, './td[10]').text
            net_inflow_of_intermediate_orders_proportion = row.find_element(By.XPATH, './td[11]').text
            net_inflow_of_small_orders_amount = row.find_element(By.XPATH, './td[12]').text
            net_inflow_of_small_orders_proportion = row.find_element(By.XPATH, './td[13]').text
            if index == 0:
                row_in_excel = ['日期', '收盘价', '涨跌幅', '主力净流入净额', '主力净流入净占比', '超大单净流入净额',
                                '超大单净流入净占比', '大单净流入净额', '大单净流入净占比', '中单净流入净额', '中单净流入净占比',
                                '小单净流入净额', '小单净流入净占比']
                write_to_excel(row_in_excel, './output/dongfangcaiwu_data.xlsx')
            row_in_excel = [date, closing_price, fluctuation_range, main_net_inflow_net_amount,
                            main_net_inflow_net_proportion, great_large_single_net_inflow_amount,
                            great_large_single_net_inflow_proportion, large_order_net_inflow_amount,
                            large_order_net_inflow_proportion, net_inflow_of_intermediate_orders_amount,
                            net_inflow_of_intermediate_orders_proportion, net_inflow_of_small_orders_amount,
                            net_inflow_of_small_orders_proportion]
            write_to_excel(row_in_excel, './output/dongfangcaiwu_data.xlsx')

