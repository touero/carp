from enum import unique, IntEnum, Enum


@unique
class DEBUG(IntEnum):
    NOT = 0
    IS = 1


@unique
class TaskType(IntEnum):
    XIA_CHU_FANG = 1  # 下厨房
    XIN_SHI_PU = 2  # 心食谱
    MEI_SHI_TIAN_XIA = 3  # 美食天下
    SHU_GUO_WANG = 4  # 蔬果网
    DONG_FANG_CAI_FU = 5  # 东方财富


@unique
class TaskUrl(Enum):
    XIA_CHU_FANG = 'https://www.xiachufang.com/explore/?page=1'
    XIN_SHI_PU = 'https://www.xinshipu.com/jiachangzuofa/16485/'
    MEI_SHI_TIAN_XIA = 'https://home.meishichina.com/recipe/guangdongxiaochi/'
    SHU_GUO_WANG = 'http://www.vegnet.com.cn/Market/477.html?page=1'
    DONG_FANG_CAI_FU = 'https://data.eastmoney.com/zjlx/600257.html'


