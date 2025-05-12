import threading
from mh_script.client_manager.launcher import Launcher
from mh_script.task_manager.dungeon_task import DungeonTask
from mh_script.task_manager.ghost_task import GhostTask
from mh_script.task_manager.daily_task import DailyTask
from mh_script.handler.basic_handler import BasicHandler
from mh_script.utils.log_util import global_log
from mh_script.utils.ocr_player import OCR_Player


def run_all_tasks_in_order():
    launcher = Launcher()
    regions = launcher.get_regions()
    if not regions:
        global_log.info("❌ 未获取到窗口区域信息")
        return

    launcher.resize_and_move_window()

    dungeon = DungeonTask(regions)
    ghost = GhostTask(regions)
    daily = DailyTask(regions)

    # 顺序执行任务
    global_log.info("▶️ 开始执行 Dungeon 任务...")
    dungeon.run(0)
    global_log.info("✅ Dungeon 任务完成！")

    global_log.info("▶️ 开始执行 Ghost 任务...")
    ghost.run(0)
    global_log.info("✅ Ghost 任务完成！")

    global_log.info("▶️ 开始执行脱离队伍...")
    BasicHandler(OCR_Player()).escape_all(regions)
    global_log.info("✅ 脱离队伍完成！")

    global_log.info("▶️ 开始执行 Daily 任务...")
    daily.run(-1)
    global_log.info("✅ Daily 任务完成！")


def main():
    # 整个流程在子线程中运行，避免主线程阻塞
    thread = threading.Thread(target=run_all_tasks_in_order, daemon=True)
    thread.start()


if __name__ == "__main__":
    main()
