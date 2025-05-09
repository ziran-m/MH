from mh_script.client_manager.launcher import Launcher
from mh_script.task_manager.dungeon_task import DungeonTask

def main():
    launcher = Launcher()

    regions = launcher.get_regions()
    if regions is None or len(regions) == 0:
        return
    launcher.resize_and_move_window()

    dungeon = DungeonTask(regions)
    dungeon.run(0)

if __name__ == "__main__":
    main()