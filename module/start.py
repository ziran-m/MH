from mh_script.client_manager.launcher import Launcher
from mh_script.utils.log_util import global_log


def main():
    global_log.info("🔵 第一步：启动并排列客户端")
    launcher = Launcher()
    launcher.start_and_arrange()


if __name__ == "__main__":
    main()
