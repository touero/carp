import platform
from dataclasses import dataclass
from enum import unique, IntEnum, Enum



@unique
class TaskType(IntEnum):
    XIA_CHU_FANG = 1  # 下厨房
    XIN_SHI_PU = 2  # 心食谱
    MEI_SHI_TIAN_XIA = 3  # 美食天下
    SHU_GUO_WANG = 4  # 蔬果网
    DONG_FANG_CAI_FU = 5  # 东方财富
    RAIL_WAY = 6  # 12306订票


@unique
class TaskUrl(Enum):
    XIA_CHU_FANG = 'https://www.xiachufang.com/explore/?page=1'
    XIN_SHI_PU = 'https://www.xinshipu.com/jiachangzuofa/16485/'
    MEI_SHI_TIAN_XIA = 'https://home.meishichina.com/recipe/guangdongxiaochi/'
    SHU_GUO_WANG = 'http://www.vegnet.com.cn/Market/477.html?page=1'
    DONG_FANG_CAI_FU = 'https://data.eastmoney.com/zjlx/600257.html'
    RAIL_WAT = 'https://kyfw.12306.cn/otn/resources/login.html'


@unique
class TaskStatus(Enum):
    SUCCESS = 'Success'
    FAIL = 'Fail'
    UNKNOWN = 'unknown'


@unique
class MachineType(Enum):
    Mac = "Darwin"
    Windows = "Windows"
    Linux = "Linux"

    @staticmethod
    def get_machine() -> str:
        system_info = platform.system()
        print(f'machine_type: {system_info}')
        for machine_type in MachineType:
            if system_info == machine_type.value:
                return machine_type.name.lower()
        return ''


@dataclass
class DataBaseInfo:
    host: str
    user: str
    password: str
    database: str
    port: int = 3306

    def __init__(self, dbinfo: dict):
        self.host = dbinfo['host']
        self.user = dbinfo['user']
        self.password = dbinfo['pwd']
        self.database = dbinfo['database']
        self.port = dbinfo['port']


@dataclass
class SmtpInfo:
    host: str
    user: str
    pwd: str
    port: int

    sender: str
    receivers: str
    from_where: str
    to_where: list
    subject: str

    def __init__(self, smtp_config: dict):
        smtp_config = smtp_config['smtp']
        smtp_service = smtp_config['smtp service']
        content = smtp_config['content']

        self.host = smtp_service['host']
        self.user = smtp_service['user']
        self.pwd = smtp_service['pass']
        self.port = smtp_service['port']

        self.sender = content['sender']
        self.receivers = content['receivers']
        self.from_where = content['from_where']
        self.to_where = content['to_where']
        self.subject = content['subject']
