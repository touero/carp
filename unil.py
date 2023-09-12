import logging
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

import openpyxl
import pytz
import os
import pymysql

from typing import List
import smtplib
from email.mime.text import MIMEText
from email.header import Header

from datetime import datetime


def log_t(args):
    """
    日志模块，等级为debug
    :param args: 仅一个参数
    :return:
    """
    if not args:
        return
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


def write_to_excel(_list: List[list], path: str):
    """
    将列表数据写入本Excel文件
    :param _list: 列表list[list]
    :param path: 存储路径
    :return:
    """
    wb = openpyxl.load_workbook(path) if os.path.exists(path) else openpyxl.Workbook()
    sheet = wb.active
    for item in _list:
        sheet.append(item)
    wb.save(path)
    log_t(f'[need_save_list]: {_list}')


def send_email(**kwargs):
    email_host = kwargs.get('mail_host')
    email_user = kwargs.get('mail_user')
    email_pass = kwargs.get('mail_pass')
    sender = kwargs.get('sender')
    # receivers = ['@.com']
    receivers = kwargs.get('receivers')
    msg = kwargs.get('msg')
    from_where = kwargs.get('from_where')
    to_where = kwargs.get('to_where')
    subject = kwargs.get('subject')
    port = kwargs.get('port')
    path = kwargs.get('path', '')

    if path:
        mail_msg = """
        <html><body><p>Crap</p>
        <p><img src="cid:image1"></p></body></html>
        """
        msg_robot = MIMEMultipart('related')
        msg_alternative = MIMEMultipart('alternative')
        msg_robot.attach(msg_alternative)
        msg_alternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))
        with open(path, 'rb') as file:
            message = MIMEImage(file.read())
        msg_robot.add_header('Content-ID', '<image1>')
        msg_robot.attach(message)
    else:
        msg_robot = MIMEText(msg, 'plain', 'utf-8')
        msg_robot['From'] = Header(from_where, 'utf-8')
        msg_robot['To'] = Header(to_where, 'utf-8')

        # subject = 'Python SMTP testing'
        msg_robot['Subject'] = Header(subject, 'utf-8')

    smtp = smtplib.SMTP()
    smtp.connect(email_host, port)
    smtp.login(email_user, email_pass)
    smtp.sendmail(sender, receivers, msg_robot.as_string())
