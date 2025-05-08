import subprocess
import time
import pygetwindow as gw
import psutil
import pyautogui

from mh_script.constant import constant
from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.log_util import global_log


class Launcher:

    def __init__(self):
        self.exe_path = constant.Constant.EXE_PATH
        self.window_title_keyword = constant.Constant.WINDOW_TITLE_KEYWORD
        self.process_name_keyword = constant.Constant.PROCESS_NAME_KEYWORD
        self.num_windows = constant.Constant.NUM_WINDOWS
        self.window_width = constant.Constant.WINDOW_WIDTH
        self.window_height = constant.Constant.WINDOW_HEIGHT
        self.windows_per_row = constant.Constant.WINDOWS_PER_ROW
        self.start_x = constant.Constant.START_X
        self.start_y = constant.Constant.START_Y
        self.x_gap = constant.Constant.X_GAP
        self.y_gap = constant.Constant.Y_GAP

    def start_clients(self, num_windows=None):
        if  num_windows is not None:
            self.num_windows = num_windows
        for i in range(self.num_windows - self.get_regions_num()):
            subprocess.Popen(self.exe_path)
            global_log.info(f"启动第 {i + 1} 个客户端...")
            time.sleep(2)

    def resize_and_move_window(self):
        global_log.info("等待游戏客户端全部启动...")
        for _ in range(10):
            windows = [w for w in gw.getWindowsWithTitle(self.window_title_keyword) if w.visible]
            if len(windows) >= self.num_windows:
                break
            time.sleep(1)

        windows = [w for w in gw.getWindowsWithTitle(self.window_title_keyword) if w.visible]
        regions = []

        if windows:
            windows = windows[:self.num_windows]
            for idx, win in enumerate(windows):
                row = idx // self.windows_per_row
                col = idx % self.windows_per_row

                x = self.start_x + col * self.x_gap
                y = self.start_y + row * self.y_gap

                global_log.info(f"调整窗口 {idx + 1} 到位置 ({x},{y})")
                win.resizeTo(self.window_width, self.window_height)
                win.moveTo(x, y)

                regions.append(ScreenRegion(
                    top=y,
                    left=x,
                    width=self.window_width,
                    height=self.window_height
                ))

            global_log.info("✅ 所有窗口排列完成！")
        else:
            global_log.info("❌ 没找到梦幻西游窗口，请检查窗口标题！")

        return regions

    def start_and_arrange(self, num_windows=None):
        self.start_clients(num_windows)
        return self.resize_and_move_window()

    def get_regions_num(self):
        global_log.info("正在查找已启动的梦幻西游窗口...")
        windows = [w for w in gw.getWindowsWithTitle(self.window_title_keyword) if w.visible]
        return len(windows)

    def get_regions(self):
        global_log.info("正在查找已启动的梦幻西游窗口...")
        windows = [w for w in gw.getWindowsWithTitle(self.window_title_keyword) if w.visible]
        regions = []

        if windows:
            windows = windows[:self.num_windows]
            for idx, win in enumerate(windows):
                row = idx // self.windows_per_row
                col = idx % self.windows_per_row

                x = self.start_x + col * self.x_gap
                y = self.start_y + row * self.y_gap

                global_log.info(f"获取窗口 {idx + 1} 的区域为 ({x},{y},{self.window_width},{self.window_height})")

                regions.append(ScreenRegion(
                    top=y,
                    left=x,
                    width=self.window_width,
                    height=self.window_height
                ))

            global_log.info("✅ 成功获取所有窗口区域信息！")
        else:
            global_log.info("❌ 未找到任何符合条件的梦幻西游窗口！")

        return regions

    def close_windows(self):
        global_log.info("正在关闭梦幻西游窗口...")

        # 查找所有符合条件的窗口并关闭它们
        windows = [w for w in gw.getWindowsWithTitle(self.window_title_keyword) if w.visible]

        if windows:
            for win in windows:
                global_log.info(f"正在关闭窗口：{win.title}")
                win.close()  # 关闭窗口
            global_log.info("✅ 成功关闭所有窗口！")
        else:
            global_log.info("❌ 未找到任何符合条件的梦幻西游窗口！")
