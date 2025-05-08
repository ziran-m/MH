import time

from task_manager.daily_task import DailyTask
from client_manager.launcher import Launcher
from mh_script.utils.log_util import log,global_log
def main():
    launcher = Launcher()
    regions = launcher.get_regions()
    if regions is None or len(regions) == 0:
        return

    # print("🟣 第二步：执行副本任务")
    # dungeon = DungeonTask(regions)
    # dungeon.run(-1)

    global_log.info("🟢 第三步：执行日常任务")
    daily = DailyTask(regions)
    daily.run(-1)

if __name__ == "__main__":
    main()
