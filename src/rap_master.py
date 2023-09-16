import traceback
import json
import uuid

from abc import ABC

from src.constants import TaskType, TaskUrl
from rpa.xiachufang_robot import XiaChuFang_Robot
from rpa.xinshipu_robot import XinShiPu_Robot
from rpa.meishitianxia_robot import MeiShiTianXia_Robot
from rpa.shuguowang_robot import ShuGuoWang_Robot
from rpa.dongfangcaifu_robot import DongFangCaiFu_Robot
from rpa.railway_robot import Railway_Robot
from src.unil import get_time_now, log_t


class RpaMaster(ABC):
    def __init__(self, **kwargs):
        self.start_time = get_time_now()
        self.end_time = None
        self.url = None
        self.robot = None
        self.config = kwargs.get('default_config')
        self.task_type = self.config.get('task_type')

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
        self.url = self.urls.get(self.task_type)
        create_robot = self.robots.get(self.task_type)
        robot = create_robot(default_config=self.config, url=self.url)
        task_uuid = uuid.uuid4()
        self.config['task_uuid'] = str(task_uuid)
        log_t(f'当前任务: 开始 {robot}, task_uuid:[{task_uuid}]')
        log_t(f"default_config =\n {json.dumps(self.config, sort_keys=False, indent=4, separators=(',', ': '))}")
        return robot

    def start_task(self):
        try:
            self.robot = self.robot_factory
            self.robot.run_task()
            task_state = 'Success'
        except Exception as e:
            task_state = 'Fail'
            log_t(e)
            log_t(traceback.print_exc())
            path = self.robot.screenshot_full_png(f'task_error.png')
            log_t(f'任务失败保存截图: {path}')
        self.end_time = get_time_now()
        log_t(f'### Task State: {task_state}, Task Cost {(self.end_time - self.start_time).seconds}s ###')