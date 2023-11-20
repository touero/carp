import traceback
import json
import uuid

from abc import ABC

from src.constants import TaskType, TaskUrl, TaskStatus
from src.robot import Robot
from rpa.xiachufang_robot import XiaChuFang_Robot
from rpa.xinshipu_robot import XinShiPu_Robot
from rpa.meishitianxia_robot import MeiShiTianXia_Robot
from rpa.shuguowang_robot import ShuGuoWang_Robot
from rpa.dongfangcaifu_robot import DongFangCaiFu_Robot
from rpa.railway_robot import Railway_Robot

from src.unil import log, calculate_time


class RpaMaster(ABC):
    _slots_ = ('start_time', 'end_time', 'url', 'robot', 'config', 'task_type')

    def __init__(self, **kwargs):
        self.url = None
        self.robot = None
        self.task_uuid = None
        self.task_state: TaskStatus = TaskStatus.UNKNOWN
        self.config: dict = kwargs.get('default_config')
        self.task_type: int = self.config.get('task_type')

        self.robots = {
            TaskType.XIA_CHU_FANG.value: XiaChuFang_Robot,
            TaskType.XIN_SHI_PU.value: XinShiPu_Robot,
            TaskType.MEI_SHI_TIAN_XIA.value: MeiShiTianXia_Robot,
            TaskType.SHU_GUO_WANG.value: ShuGuoWang_Robot,
            TaskType.DONG_FANG_CAI_FU.value: DongFangCaiFu_Robot,
            TaskType.RAIL_WAY.RAIL_WAY: Railway_Robot
        }

        self.urls = {
            TaskType.XIA_CHU_FANG.value: TaskUrl.XIA_CHU_FANG.value,
            TaskType.XIN_SHI_PU.value: TaskUrl.XIN_SHI_PU.value,
            TaskType.MEI_SHI_TIAN_XIA.value: TaskUrl.MEI_SHI_TIAN_XIA.value,
            TaskType.SHU_GUO_WANG.value: TaskUrl.SHU_GUO_WANG.value,
            TaskType.DONG_FANG_CAI_FU.value: TaskUrl.DONG_FANG_CAI_FU.value,
            TaskType.RAIL_WAY.value: TaskUrl.RAIL_WAT.value
        }

    @property
    def robot_factory(self):
        self.url: str = self.urls.get(self.task_type)
        robot: Robot = self.robots.get(self.task_type)(default_config=self.config, url=self.url)
        self.task_uuid = str(uuid.uuid4())
        self.config['task_uuid'] = self.task_uuid
        log(f'当前任务: 开始 {robot}, task_uuid:[{self.task_uuid}]')
        log(f"default_config =\n {json.dumps(self.config, sort_keys=False, indent=4, separators=(',', ': '))}")
        return robot

    @calculate_time
    def start_task(self):
        try:
            self.robot = self.robot_factory
            self.robot.run_task()
            self.robot.task_finish()
            self.task_state = TaskStatus.SUCCESS
        except Exception as e:
            self.task_state = TaskStatus.FAIL
            log(f'{str(e)}')
            log(traceback.format_exc())
            path = self.robot.screenshot_full_png(f'task_error.png')
            log(f'任务失败保存截图: {path}')
