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
}

if __name__ == '__main__':
    RpaMaster(default_config=default_config).start_task()

