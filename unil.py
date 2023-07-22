import logging
from datetime import datetime
import openpyxl
import pytz
import os
from dataclasses import dataclass
import pymysql
import traceback


def log_t(args):
    """
    日志模块，等级为debug
    :param args: 仅一个参数
    :return:
    """
    logger = logging.getLogger('rpa')
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(filename='log/rpa.log',
                                       encoding='UTF-8')
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logger.debug(f"{args}")
    logger.removeHandler(file_handler)
    logger.removeHandler(console_handler)


@property
def get_time_now() -> datetime:
    """
    获取当前日期
    :return: datetime
    """
    return datetime.now(pytz.timezone('Asia/Shanghai')).now()


def get_time_now_str(args: datetime) -> str:
    """
    获取当前日期
    :param args: datetime类型的参数
    :return: str
    """
    return args.strftime('%Y-%m-%d %H:%M:%S')


# 将字典数据写入本地MySQL，传入字典与表即可
def write_tolocal_mysql(dc, table):
    # todo 这个模块将会被移除，请转到SqlMaster
    keys = ','.join(dc.keys())
    values = list(dc.values())
    values = str(values).split("[")[1]
    values = values.split("]")[0]
    conn = pymysql.connect(host='localhost', user='root', password='root', db='food', port=3306)
    cursor = conn.cursor()
    sql = f'INSERT INTO {table}({keys}) VALUES ({values});'.format(table, keys, values)
    cursor.execute(sql)
    conn.commit()
    conn.close()


def write_to_excel(_list: list, path: str):
    """
    将列表数据写入本Excel文件
    :param _list: 列表
    :param path: 存储路径
    :return:
    """
    wb = openpyxl.load_workbook(path) if os.path.exists(path) else openpyxl.Workbook()
    sheet = wb.active
    sheet.append(_list)
    wb.save(path)
