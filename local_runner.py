from rap_master import RpaMaster
"""
task_type
    1:下厨房
    2:心食谱
    3:美食天下
    4:蔬果网
    5:东方财务
"""
default_config = {
    "task_type": 5,
    "is_debug": 1,
    "sql_info": {
        "state": 0,
        "host": "localhost",
        "user": "root",
        "password": "root",
        "database": "food",
        "port": 3306
    }
}

if __name__ == '__main__':
    created_robot = RpaMaster(default_config)
    robot = created_robot.robot_factory()
    robot.run_task()
