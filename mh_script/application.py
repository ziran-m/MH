import time

from task_manager.daily_task import DailyTask
from client_manager.launcher import Launcher
from mh_script.utils.log_util import log,global_log
def main():
    global_log.info("🔵 第一步：启动并排列客户端")
    launcher = Launcher()
    regions = launcher.start_and_arrange()

    # ⏳ 插入等待，手动完成必要操作
    global_log.info("\n🔔 请在游戏中完成必要的准备操作，比如：登录、选角色、调整设置...")
    input("👉 完成后按回车继续...")


    # 或者自动检测某个条件，比如检测界面出现什么按钮（如果你想全自动的话）

    # print("🟣 第二步：执行副本任务")
    # dungeon = DungeonTask(regions)
    # dungeon.run(-1)

    global_log.info("🟢 第三步：执行日常任务")
    daily = DailyTask(regions)
    daily.run(-1)

    global_log.info("🟢 第三步：执行日常任务")
    launcher.close_windows()

if __name__ == "__main__":
    main()
