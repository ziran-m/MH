import threading
from mh_script.client_manager.launcher import Launcher
from mh_script.task_manager.ghost_task import GhostTask


def run_ghost_in_thread(task, idx):
    thread = threading.Thread(target=task.run, args=(idx,), daemon=True)
    thread.start()


def main():
    launcher = Launcher()
    regions = launcher.get_regions()
    if not regions:
        return

    launcher.resize_and_move_window()

    task = GhostTask(regions)
    run_ghost_in_thread(task, 0)  # 使用子线程执行任务，避免主线程卡死


if __name__ == "__main__":
    main()
