import logging
from email.mime.application import MIMEApplication
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


def write_to_excel(_list: List[list], filename: str):
    """
    将列表数据写入本Excel文件, 保存在output/
    :param _list: 列表list[list]
    :param filename: 文件名
    :return:
    """
    log_t(f'download dir: {filename}')
    path = f'./output/{filename}'
    wb = openpyxl.load_workbook(path) if os.path.exists(path) else openpyxl.Workbook()
    sheet = wb.active
    for item in _list:
        sheet.append(item)
    wb.save(path)
    log_t(f'[need_save_list]: {_list}')


def send_email(smtp_info, msg: str = None, img: str = None, file: str = None):
    if img:
        with open('src/email_content.html', encoding='utf-8') as file:
            email_msg = file.read()
        msg_robot = MIMEMultipart('related')
        msg_alternative = MIMEMultipart('alternative')
        msg_robot.attach(msg_alternative)
        msg_alternative.attach(MIMEText(email_msg, 'html', 'utf-8'))
        with open(img, 'rb') as file:
            message = file.read()
        image_part = MIMEImage(message, name='image.png')
        msg_robot.add_header('Content-ID', '<image1>')
        msg_robot.attach(image_part)

    elif msg:
        msg_robot = MIMEText(f'{msg}, https://github.com/weiensong/carp', 'plain', 'utf-8')

    elif file:
        msg = "This is an email with attachments from carp, https://github.com/weiensong/carp"
        msg_text = MIMEText(msg, 'plain')
        msg_robot = MIMEMultipart()
        file_name = file.split('/')[-1]
        with open(file, 'rb') as f:
            part = MIMEApplication(f.read(), Name=f'{file_name}')
        part['Content-Disposition'] = f'attachment; filename={file_name}'
        msg_robot.attach(msg_text)
        msg_robot.attach(part)
    else:
        log_t('sending email failed')
        return

    msg_robot['From'] = Header(smtp_info.from_where)
    msg_robot['To'] = Header(', '.join(smtp_info.to_where), 'utf-8')
    msg_robot['Subject'] = Header(smtp_info.subject, 'utf-8')

    smtp = smtplib.SMTP(smtp_info.host, smtp_info.port)
    smtp.starttls()
    smtp.login(smtp_info.user, smtp_info.pwd)
    smtp.sendmail(smtp_info.sender, smtp_info.receivers, msg_robot.as_string())
    result = msg if msg else img if img else file
    log_t(f'[sending email success: {result}]')
