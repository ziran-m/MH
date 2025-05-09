from mh_script.client_manager.launcher import Launcher
from mh_script.handler.basic_handler import BasicHandler
from mh_script.task_manager.daily_task import DailyTask
from mh_script.task_manager.dungeon_task import DungeonTask
from mh_script.task_manager.ghost_task import GhostTask
from mh_script.utils.log_util import global_log
from mh_script.utils.ocr_player import OCR_Player


def main():
    launcher = Launcher()
    ocr_player = OCR_Player()
    basic_handler = BasicHandler(ocr_player)
    #获取窗口
    regions = launcher.get_regions()
    if regions is None or len(regions) == 0:
        return
    # 调整排列窗口
    launcher.resize_and_move_window()
    # 副本
    dungeon = DungeonTask(regions)
    dungeon.run(0)
    # 抓鬼
    ghost = GhostTask(regions)
    ghost.run(0)
    # 脱离队伍
    basic_handler.escape_all(regions)
    # 日常
    task = DailyTask(regions)
    task.run(-1)
    global_log.info("320完成")


if __name__ == "__main__":
    main()