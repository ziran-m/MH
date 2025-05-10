from mh_script.client_manager.launcher import Launcher
from mh_script.task_manager.daily_task import DailyTask
from mh_script.utils.ocr_player import OCR_Player

def main():
    launcher = Launcher()

    regions = launcher.get_regions()
    if regions is None or len(regions) == 0:
        return
    launcher.resize_and_move_window()
    task = DailyTask(regions)
    task.run(-1)

if __name__ == "__main__":
    main()