import threading
from mh_script.client_manager.launcher import Launcher
from mh_script.task_manager.dungeon_task import DungeonTask


def run_dungeon_in_thread(dungeon, idx):
    thread = threading.Thread(target=dungeon.run, args=(idx,), daemon=True)
    thread.start()


def main():
    launcher = Launcher()
    regions = launcher.get_regions()
    if not regions:
        return

    launcher.resize_and_move_window()

    dungeon = DungeonTask(regions)
    run_dungeon_in_thread(dungeon, 0)  # 在子线程中运行任务


if __name__ == "__main__":
    main()
