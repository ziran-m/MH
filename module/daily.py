import threading

from mh_script.client_manager.launcher import Launcher
from mh_script.task_manager.daily_task import DailyTask


def run_task_in_thread(task, idx):
    thread = threading.Thread(target=task.run, args=(idx,), daemon=True)
    thread.start()


def main():
    launcher = Launcher()
    regions = launcher.get_regions()
    if not regions:
        return

    launcher.resize_and_move_window()

    task = DailyTask(regions)
    run_task_in_thread(task, -1)  # 在子线程中执行耗时任务


if __name__ == "__main__":
    main()
