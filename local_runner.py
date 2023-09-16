import yaml

from argparse import ArgumentParser
from rap_master import RpaMaster
"""
task_type
    [1]:下厨房 [2]:心食谱 [3]:美食天下 [4]:蔬果网 [5]:东方财务 [6]:12306

12306_info
    [travel_person]: 乘车人，目前支持一人，且无法区分学生票和成人票 [site]: 座位，即A、B、C、D和F start_station：出发地
    [to_station]: 目的地 [travel_date]: 发车日期 [start_time]: 发车时间[to_time]: 到达时间
    请写具体些目前只适配那么多，严格要求按照12306填写。
    考虑安全问题，网站目前只支持手机扫描二维码登录，等待扫描二维码时间为60秒
"""
default_config = {
    "task_type": 6,
    "12306_info": {
            'travel_person': '',
            'seat': 'F',
            'start_station': '',
            'to_station': '',
            'travel_date': '2023-02-31',
            'start_time': '17:40',
            'to_time': '18:47'
        },
}
email: bool = True
parser = ArgumentParser()
parser.add_argument('--smtp_config', '-y', default='config/smtp.yaml', help='smtp config')
if __name__ == '__main__':
    if email:
        smtp_args = parser.parse_args()
        smtp_config = yaml.load(open(smtp_args.smtp_config, encoding='utf8'), yaml.FullLoader)
        default_config['smtp_config'] = smtp_config

    RpaMaster(default_config=default_config).start_task()

