from .robot import Robot
from src.tools import write_to_excel


class DongFangCaiFu_Robot(Robot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        return '东方财经'

    def run_task(self):
        rows = self.wait_elements_by_xpath('//div[@id="table_ls"]//tbody//tr')
        header_line = ['日期', '收盘价', '涨跌幅', '主力净流入净额', '主力净流入净占比', '超大单净流入净额',
                       '超大单净流入净占比', '大单净流入净额', '大单净流入净占比', '中单净流入净额', '中单净流入净占比',
                       '小单净流入净额', '小单净流入净占比']
        self.need_save_list.append(header_line)
        for row in rows:
            self.scroll_to_element_safe(row)

            date = row.find_element('./td[1]').text
            closing_price = row.find_element('./td[2]').text
            fluctuation_range = row.find_element('./td[3]').text
            main_net_inflow_net_amount = row.find_element('./td[4]').text
            main_net_inflow_net_proportion = row.find_element('./td[5]').text
            great_large_single_net_inflow_amount = row.find_element('./td[6]').text
            great_large_single_net_inflow_proportion = row.find_element('./td[7]').text
            large_order_net_inflow_amount = row.find_element('./td[8]').text
            large_order_net_inflow_proportion = row.find_element('./td[9]').text
            net_inflow_of_intermediate_orders_amount = row.find_element('./td[10]').text
            net_inflow_of_intermediate_orders_proportion = row.find_element('./td[11]').text
            net_inflow_of_small_orders_amount = row.find_element('./td[12]').text
            net_inflow_of_small_orders_proportion = row.find_element('./td[13]').text

            row_in_excel = [date, closing_price, fluctuation_range, main_net_inflow_net_amount,
                            main_net_inflow_net_proportion, great_large_single_net_inflow_amount,
                            great_large_single_net_inflow_proportion, large_order_net_inflow_amount,
                            large_order_net_inflow_proportion, net_inflow_of_intermediate_orders_amount,
                            net_inflow_of_intermediate_orders_proportion, net_inflow_of_small_orders_amount,
                            net_inflow_of_small_orders_proportion]
            self.need_save_list.append(row_in_excel)

        write_to_excel(self.need_save_list, 'dongfangcaiwu_data.xlsx')
        self.update_info_by_email(file='output/dongfangcaiwu_data.xlsx')
