import threading

from mh_script.client_manager.launcher import Launcher
from mh_script.handler.wabao_handler import WaBao

def run_in_thread(task, region):
    thread = threading.Thread(target=task.do, args=(region,), daemon=True)
    thread.start()


def main():
    launcher = Launcher()
    regions = launcher.get_regions()
    if not regions:
        return

    launcher.resize_and_move_window()

    task = WaBao(regions)
    run_in_thread(task, regions[0])  # 使用子线程执行任务，避免主线程卡死


if __name__ == "__main__":
    main()