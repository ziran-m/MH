from mh_script.client_manager.launcher import Launcher
from mh_script.task_manager.daily_task import DailyTask
from mh_script.utils.ocr_player import OCR_Player

if __name__ == "__main__":
    launcher = Launcher()
    regions = launcher.get_regions()
    ocr_player = OCR_Player()
    task = DailyTask(regions)
    task.run(0)