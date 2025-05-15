import threading
from mh_script.client_manager.launcher import Launcher
from mh_script.utils.log_util import global_log


def task():
    global_log.info("🔵 第一步：启动并排列客户端")
    launcher = Launcher()
    launcher.start_and_arrange()


def main():
    # 创建子线程，执行 task 函数
    thread = threading.Thread(target=task)
    thread.start()
    # 如果需要主线程等待子线程完成，调用 thread.join()
    # thread.join()


if __name__ == "__main__":
    main()
