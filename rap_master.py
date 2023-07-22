from rpa.xiachufang_robot import XiaChuFang_Robot
from constants import TaskType, TaskUrl
from rpa.xinshipu_robot import XinShiPu_Robot
from rpa.meishitianxia_robot import MeiShiTianXia_Robot
from rpa.shuguowang_robot import ShuGuoWang_Robot
from rpa.dongfangcaifu_robot import DongFangCaiFu_Robot
from unil import log_t
from abc import ABC
import json


class RpaMaster(ABC):
    def __init__(self, **kwargs):
        self.url = None
        self.robot = None
        self.config = kwargs.get('default_config')
        self.task_type = self.config.get('task_type')
        self.sql_state = self.config.get('sql_info').get('state')

        self.robots = {
            TaskType.XIA_CHU_FANG.value: XiaChuFang_Robot,
            TaskType.XIN_SHI_PU.value: XinShiPu_Robot,
            TaskType.MEI_SHI_TIAN_XIA.value: MeiShiTianXia_Robot,
            TaskType.SHU_GUO_WANG.value: ShuGuoWang_Robot,
            TaskType.DONG_FANG_CAI_FU.value: DongFangCaiFu_Robot
        }

        self.urls = {
            TaskType.XIA_CHU_FANG.value: TaskUrl.XIA_CHU_FANG.value,
            TaskType.XIN_SHI_PU.value: TaskUrl.XIN_SHI_PU.value,
            TaskType.MEI_SHI_TIAN_XIA.value: TaskUrl.MEI_SHI_TIAN_XIA.value,
            TaskType.SHU_GUO_WANG.value: TaskUrl.SHU_GUO_WANG.value,
            TaskType.DONG_FANG_CAI_FU.value: TaskUrl.DONG_FANG_CAI_FU.value
        }
        # todo 需要sql 最好写成装饰器
        # self.sql_state = None
        # if self.sql_state == SqlState.ON:
        #     self.sql_master = SqlMaster(self.config)

    @property
    def robot_factory(self):
        try:
            self.url = self.urls.get(self.task_type)
            Robot = self.robots.get(self.task_type)
            self.robot = Robot(default_config=self.config, url=self.url)
            log_t(f'开始_{self.robot.__str__()}')
            log_t(f"default_config =\n {json.dumps(self.config, sort_keys=True, indent=4, separators=(',', ': '))}")
            return self.robot
        except Exception as e:
            log_t(e)
