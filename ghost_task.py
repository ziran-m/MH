from mh_script.client_manager.launcher import Launcher
from mh_script.task_manager.ghost_task import GhostTask

def main():
    launcher = Launcher()

    regions = launcher.get_regions()
    if regions is None or len(regions) == 0:
        return
    launcher.resize_and_move_window()
    task = GhostTask(regions)
    task.run(0)

if __name__ == "__main__":
    main()