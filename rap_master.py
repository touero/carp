from rpa.xiachufang_robot import XiaChuFang_Robot
from constants import TaskType, TaskUrl, SqlState
from rpa.xinshipu_robot import XinShiPu_Robot
from rpa.meishitianxia_robot import MeiShiTianXia_Robot
from rpa.shuguowang_robot import ShuGuoWang_Robot
from rpa.dongfangcaifu_robot import DongFangCaiFu_Robot
from unil import log_t
from abc import ABC


class RpaMaster(ABC):
    def __init__(self, default_config):
        self.config = default_config
        log_t(f'default_config = {self.config}')
        self.task_type = self.config.get('task_type')
        self.sql_state = self.config.get('sql_info').get('state')
        self.robot = None
        # todo 需要sql
        # self.sql_state = None
        # if self.sql_state == SqlState.ON:
        #     self.sql_master = SqlMaster(self.config)

    def robot_factory(self):
        try:
            if self.task_type == TaskType.XIA_CHU_FANG.value:
                self.robot = XiaChuFang_Robot(self.config, TaskUrl.XIA_CHU_FANG.value)
            elif self.task_type == TaskType.XIN_SHI_PU.value:
                self.robot = XinShiPu_Robot(self.config, TaskUrl.XIN_SHI_PU.value)
            elif self.task_type == TaskType.MEI_SHI_TIAN_XIA.value:
                self.robot = MeiShiTianXia_Robot(self.config, TaskUrl.MEI_SHI_TIAN_XIA.value)
            elif self.task_type == TaskType.SHU_GUO_WANG.value:
                self.robot = ShuGuoWang_Robot(self.config, TaskUrl.SHU_GUO_WANG.value)
            elif self.task_type == TaskType.DONG_FANG_CAI_FU.value:
                self.robot = DongFangCaiFu_Robot(self.config, TaskUrl.DONG_FANG_CAI_FU.value)
            return self.robot
        except Exception as e:
            log_t(e)
