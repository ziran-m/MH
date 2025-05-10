from mh_script.client_manager.launcher import Launcher
from mh_script.utils.log_util import global_log


def main():
    global_log.info("🟢 第四步：关闭程序")
    launcher = Launcher()
    launcher.close_windows()


if __name__ == "__main__":
    main()
