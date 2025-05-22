import warnings

from mh_script.handler.baotu_handler import BaoTu
from mh_script.handler.dati_handler import DaTi
from mh_script.handler.mijing_handler import MiJing
from mh_script.handler.yabiao_handler import YaBiao

warnings.filterwarnings("ignore",
    message="No ccache found",
    module="paddle.utils.cpp_extension")

import json
import os
import threading
import customtkinter as ctk

from mh_script.client_manager.launcher import Launcher
from mh_script.constant.constant import Constant
from mh_script.handler.basic_handler import BasicHandler
from mh_script.handler.wabao_handler import WaBao
from mh_script.handler.red_lls_handler import RedLLS
from mh_script.task_manager.daily_task import DailyTask
from mh_script.task_manager.dungeon_task import DungeonTask
from mh_script.task_manager.ghost_task import GhostTask
from mh_script.utils.log_util import TextHandler, logger, global_log
from mh_script.utils.ocr_player import OCR_Player


class App:
    def __init__(self):
        self.config_file = "config.json"
        self.config_data = self.load_config()
        self.launcher = Launcher()
        self.ocrPlayer = OCR_Player()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.root = ctk.CTk()
        self.root.geometry("500x400")
        self.root.title("脚本启动器[当前只支持2k显示器]")

        self.font_style = ("Microsoft YaHei", 14)
        self.button_config = {
            "font": self.font_style,
            "height": 30,
            "corner_radius": 0,
            "fg_color": "transparent",  # 与背景一致
            "hover_color": "#3a3a3a",  # 灰色，hover 时显现
            "text_color": "white",  # 文字保持白色可读
            "bg_color": "transparent"  # 避免覆盖父容器背景
        }
        self.label_config = {
            "font": self.font_style,
            "height": 30,
            "corner_radius": 0,
            "fg_color": "transparent",  # 与背景一致
            "text_color": "white",  # 文字保持白色可读
            "bg_color": "transparent",  # 避免覆盖父容器背景
            "anchor": "w"  # 设置文字靠左对齐
        }
        self.entry_config = {
            "font": self.font_style,
            "height": 30,
            "corner_radius": 0,
            "border_width": 0,  # 去除边框
            "fg_color": "transparent",  # 背景透明
            "text_color": "white",  # 字体颜色
            "bg_color": "transparent",  # 背景透明
        }

        self.setup_layout()

        self.create_buttons()

        self.create_log_ui()

        self.create_daily_ui()
        self.create_config_ui()

        self.root.mainloop()

    def setup_layout(self):

        # 左边按钮区域
        self.left_frame = ctk.CTkFrame(self.root)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

        # 右边日志区域
        self.right_frame = ctk.CTkFrame(self.root)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # 让日志区随窗口伸缩
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        # 配置页面
        self.config_frame = ctk.CTkFrame(self.root)
        self.config_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")
        self.config_frame.grid_remove()  # 默认隐藏

        # 日常明细页面
        self.daily_frame = ctk.CTkFrame(self.root)
        self.daily_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")
        self.daily_frame.grid_remove()  # 默认隐藏

    # 主页面
    def create_buttons(self):

        row = 0
        self.open_button = ctk.CTkButton(self.left_frame, text="启动", command=self.start_task, **self.button_config)
        self.open_button.grid(row=row, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
        row += 1
        self.button_320 = ctk.CTkButton(self.left_frame, text="320", command=self.task_320, **self.button_config)
        self.button_320.grid(row=row, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
        row += 1
        self.dungeon_task_button = ctk.CTkButton(self.left_frame, text="副本", command=self.dungeon_task_task,
                                                 **self.button_config)
        self.dungeon_task_button.grid(row=row, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
        row += 1
        self.ghost_button = ctk.CTkButton(self.left_frame, text="抓鬼", command=self.ghost_task, **self.button_config)
        self.ghost_button.grid(row=row, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
        row += 1
        # 日常按钮跨越两列
        self.show_daily_button = ctk.CTkButton(self.left_frame, text="日常", command=self.show_daily_ui, **self.button_config)
        self.show_daily_button.grid(row=row, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
        row += 1
        self.kaogu_button = ctk.CTkButton(self.left_frame, text="考古", command=self.kaogu_task, **self.button_config)
        self.kaogu_button.grid(row=row, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
        row += 1
        self.lls_button = ctk.CTkButton(self.left_frame, text="玲珑石", command=self.lls_task, **self.button_config)
        self.lls_button.grid(row=row, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
        row += 1
        self.config_button = ctk.CTkButton(self.left_frame, text="配置", command=self.show_config_ui,
                                           **self.button_config)
        self.config_button.grid(row=row, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

        # 添加退出按钮到 left_frame（假设 row 是从上往下排的）
        self.exit_button = ctk.CTkButton(self.left_frame, text="退出", command=self.root.destroy, **self.button_config)
        self.exit_button.grid(row=99, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

        # 主页面

    def create_daily_ui(self):

        row = 0
        # 日常按钮跨越两列
        self.daily_button = ctk.CTkButton(self.daily_frame, text="全部", command=self.daily_task, **self.button_config)
        self.daily_button.grid(row=row, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
        row += 1
        self.baotu_button = ctk.CTkButton(self.daily_frame, text="宝图", command=self.baotu_task, **self.button_config)
        self.baotu_button.grid(row=row, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

        row += 1
        self.wabao_button = ctk.CTkButton(self.daily_frame, text="挖宝", command=self.dig_task,
                                          **self.button_config)
        self.wabao_button.grid(row=row, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
        row += 1
        # 日常按钮跨越两列
        self.mijing_button = ctk.CTkButton(self.daily_frame, text="秘境", command=self.mijing_task, **self.button_config)
        self.mijing_button.grid(row=row, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

        row += 1
        self.yabiao_button = ctk.CTkButton(self.daily_frame, text="押镖", command=self.yabiao_task, **self.button_config)
        self.yabiao_button.grid(row=row, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

        row += 1
        self.dati_button = ctk.CTkButton(self.daily_frame, text="答题", command=self.dati_task, **self.button_config)
        self.dati_button.grid(row=row, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
        # 返回按钮
        self.daily_back_button = ctk.CTkButton(self.daily_frame, text="返回", command=self.show_main_ui,
                                         **self.button_config)
        self.daily_back_button.grid(row=99, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
    # 日志页面
    def create_log_ui(self):
        """创建日志区域（文本框和滚动条）"""

        # 日志框 + 滚动条放入一个单独的 Frame 内
        log_frame = ctk.CTkFrame(self.right_frame)
        log_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")  # 占满右侧

        log_frame.grid_rowconfigure(0, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)

        # 文本框
        self.log_text = ctk.CTkTextbox(log_frame, font=self.font_style, wrap="word", state="normal")
        self.log_text.grid(row=0, column=0, sticky="nsew")

        # 最外层布局
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

        # 设置日志 handler
        self.log_text_handler = TextHandler(self.log_text)
        logger.addHandler(self.log_text_handler)

    # 配置
    def create_config_ui(self):
        self.config_frame.grid_columnconfigure(0, weight=1)
        self.config_frame.grid_columnconfigure(1, weight=1)
        """创建配置界面但默认隐藏"""

        row = 0
        self.dungeon_task_Label = ctk.CTkLabel(self.config_frame, text="副本起始点", **self.label_config)
        self.dungeon_task_Label.grid(row=row, column=0, padx=10, pady=(0, 10), sticky="ew")

        # 副本输入框放在副本按钮旁边
        self.dungeon_num_entry = ctk.CTkEntry(self.config_frame, placeholder_text="0 侠士 1 普本",
                                              **self.entry_config)
        self.dungeon_num_entry.grid(row=row, column=1, padx=10, pady=(0, 10), sticky="ew")
        dungeon_start = self.config_data.get("dungeon_start", "")
        if dungeon_start:  # 有值才插入
            self.dungeon_num_entry.insert(0, dungeon_start)

        row += 1
        self.ghost_num_Label = ctk.CTkLabel(self.config_frame, text="抓鬼轮数", **self.label_config)
        self.ghost_num_Label.grid(row=row, column=0, padx=10, pady=(0, 10), sticky="ew")

        # 抓鬼轮数输入框放在抓鬼按钮旁边
        self.ghost_num_entry = ctk.CTkEntry(self.config_frame, placeholder_text="2", **self.entry_config)
        self.ghost_num_entry.grid(row=row, column=1, padx=10, pady=(0, 10), sticky="ew")
        ghost_rounds = self.config_data.get("ghost_rounds", "")
        if ghost_rounds:
            self.ghost_num_entry.insert(0, ghost_rounds)

        row += 1
        self.app_path_Label = ctk.CTkLabel(self.config_frame, text="文件运行地址", **self.label_config)
        self.app_path_Label.grid(row=row, column=0, padx=10, pady=(0, 10), sticky="ew")

        # 文件运行地址输入框
        self.app_path_entry = ctk.CTkEntry(self.config_frame, placeholder_text="请输入文件运行地址",
                                           **self.entry_config)
        self.app_path_entry.grid(row=row, column=1, padx=10, pady=(0, 10), sticky="ew")
        app_path = self.config_data.get("app_path", "")
        if app_path:
            self.app_path_entry.insert(0, app_path)

        row += 1
        self.save_button = ctk.CTkButton(self.config_frame, text="保存配置", command=self.save_config,
                                         **self.button_config)
        self.save_button.grid(row=99, column=0, padx=10, pady=(0, 10), sticky="ew")
        # 返回按钮
        self.back_button = ctk.CTkButton(self.config_frame, text="返回", command=self.show_main_ui,
                                         **self.button_config)
        self.back_button.grid(row=99, column=1, padx=10, pady=(0, 10), sticky="ew")

    def save_config(self):
        self.config_data["dungeon_start"] = self.dungeon_num_entry.get()
        self.config_data["ghost_rounds"] = self.ghost_num_entry.get()
        self.config_data["app_path"] = self.app_path_entry.get()

        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.config_data, f, ensure_ascii=False, indent=2)

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return {}  # 默认空配置

    def show_config_ui(self):
        """显示配置界面，隐藏主按钮区域"""
        self.left_frame.grid_remove()
        self.config_frame.grid()

    def show_daily_ui(self):
        """显示配置界面，隐藏主按钮区域"""
        self.left_frame.grid_remove()
        self.daily_frame.grid()

    def show_main_ui(self):
        """返回主按钮区域，隐藏配置界面"""
        self.config_frame.grid_remove()
        self.daily_frame.grid_remove()
        self.left_frame.grid()

    def start_task(self):
        """启动任务（对应 '启动' 按钮）"""
        self.disable_buttons_temporarily()  # 禁用按钮

        val = self.config_data.get("app_path", "").strip()
        if  val:
            Constant.EXE_PATH = val
        global_log.info(f"应用程序启动地址：{Constant.EXE_PATH}")

        def task():
            global_log.info("🔵 第一步：启动并排列客户端")
            launcher = Launcher()
            launcher.start_and_arrange()

        thread = threading.Thread(target=task)
        thread.start()
        return thread

    def daily_task(self):
        self.disable_buttons_temporarily()  # 禁用按钮

        regions = self.launcher.get_regions()
        if not regions:
            return

        self.launcher.resize_and_move_window()

        task = DailyTask(regions)

        # 启动线程执行耗时任务
        thread = threading.Thread(target=task.run, args=(-1,), daemon=True)
        thread.start()
        return thread

    def dungeon_task_task(self):
        """副本任务（对应 '关闭' 按钮）"""
        self.disable_buttons_temporarily()  # 禁用按钮

        val = self.config_data.get("dungeon_num", "").strip()
        if  val:
            Constant.DUNGEON_NUM = val
        global_log.info(f"副本轮数设置为：{Constant.DUNGEON_NUM}")

        regions = self.launcher.get_regions()
        if not regions:
            return

        self.launcher.resize_and_move_window()

        dungeon = DungeonTask(regions)
        thread = threading.Thread(target=dungeon.run, args=(0,), daemon=True)
        thread.start()

    def ghost_task(self):
        """关闭任务（对应 '关闭' 按钮）"""
        self.disable_buttons_temporarily()  # 禁用按钮

        val = int(self.ghost_num_entry.get().strip())
        if  val:
            Constant.GHOST_NUM = val
        logger.info(f"抓鬼轮数设置为：{Constant.GHOST_NUM}")

        regions = self.launcher.get_regions()
        if not regions:
            return

        self.launcher.resize_and_move_window()

        task = GhostTask(regions)
        thread = threading.Thread(target=task.run, args=(0,), daemon=True)
        thread.start()

    def task_320(self):
        def run_all_tasks_in_order():
            regions = self.launcher.get_regions()
            if not regions:
                global_log.info("❌ 未获取到窗口区域信息")
                return

            self.launcher.resize_and_move_window()

            dungeon = DungeonTask(regions)
            ghost = GhostTask(regions)
            daily = DailyTask(regions)

            # 顺序执行任务
            global_log.info("▶️ 开始执行 Dungeon 任务...")
            dungeon.run(0)
            global_log.info("✅ Dungeon 任务完成！")

            global_log.info("▶️ 开始执行 Ghost 任务...")
            ghost.run(0)
            global_log.info("✅ Ghost 任务完成！")

            BasicHandler(OCR_Player()).escape_all(regions)

            global_log.info("▶️ 开始执行 Daily 任务...")
            daily.run(-1)
            global_log.info("✅ Daily 任务完成！")

        """320任务（对应 '320' 按钮）"""
        self.disable_buttons_temporarily()  # 禁用按钮

        try:
            val1 =int (self.config_data.get("dungeon_start", "0").strip())
        except ValueError:
            val1 = 0

        try:
            val2 =int (self.config_data.get("ghost_num", "2").strip())
        except ValueError:
            val2 = 2

        Constant.DUNGEON_NUM = val1

        Constant.GHOST_NUM = val2

        global_log.info(f"副本轮数设置为：{Constant.DUNGEON_NUM}")

        # 整个流程在子线程中运行，避免主线程阻塞
        thread = threading.Thread(target=run_all_tasks_in_order, daemon=True)
        thread.start()



    def kaogu_task(self):
        """考古任务"""
        self.disable_buttons_temporarily()
        regions = self.launcher.get_regions()
        if not regions:
            return

        self.launcher.resize_and_move_window()

        task = WaBao(self.ocrPlayer)
        thread = threading.Thread(target=task.do, args=(regions[0],), daemon=True)
        thread.start()
    def lls_task(self):
        """玲珑石"""
        self.disable_buttons_temporarily()
        regions = self.launcher.get_regions()
        if not regions:
            return

        self.launcher.resize_and_move_window()

        task = RedLLS(self.ocrPlayer)
        thread = threading.Thread(target=task.do, args=(regions[0],), daemon=True)
        thread.start()

    def baotu_task(self):
        """宝图"""
        self.disable_buttons_temporarily()
        regions = self.launcher.get_regions()
        if not regions:
            return

        self.launcher.resize_and_move_window()

        task = BaoTu(self.ocrPlayer)
        thread = threading.Thread(target=task.do_all, args=(regions,), daemon=True)
        thread.start()

    def dig_task(self):
        """挖宝图"""
        self.disable_buttons_temporarily()
        regions = self.launcher.get_regions()
        if not regions:
            return

        self.launcher.resize_and_move_window()

        task = BaoTu(self.ocrPlayer)
        thread = threading.Thread(target=task.dig_all, args=(regions,), daemon=True)
        thread.start()

    def mijing_task(self):
        """秘境"""
        self.disable_buttons_temporarily()
        regions = self.launcher.get_regions()
        if not regions:
            return

        self.launcher.resize_and_move_window()

        task = MiJing(self.ocrPlayer)
        thread = threading.Thread(target=task.do_all, args=(regions,), daemon=True)
        thread.start()

    def yabiao_task(self):
        """押镖"""
        self.disable_buttons_temporarily()
        regions = self.launcher.get_regions()
        if not regions:
            return

        self.launcher.resize_and_move_window()

        task = YaBiao(self.ocrPlayer)
        thread = threading.Thread(target=task.do_all, args=(regions,), daemon=True)
        thread.start()

    def dati_task(self):
        """答题"""
        self.disable_buttons_temporarily()
        regions = self.launcher.get_regions()
        if not regions:
            return

        self.launcher.resize_and_move_window()

        task = DaTi(self.ocrPlayer)
        thread = threading.Thread(target=task.do_all, args=(regions,), daemon=True)
        thread.start()

    def disable_buttons_temporarily(self):
        """禁用按钮并在1秒后重新启用"""
        self.open_button.configure(state="disabled")
        self.daily_button.configure(state="disabled")
        self.dungeon_task_button.configure(state="disabled")
        self.button_320.configure(state="disabled")
        self.ghost_button.configure(state="disabled")
        self.kaogu_button.configure(state="disabled")
        self.lls_button.configure(state="disabled")
        self.app_path_entry.configure(state="disabled")
        self.config_button.configure(state="disabled")
        self.baotu_button.configure(state="disabled")
        self.yabiao_button.configure(state="disabled")
        self.mijing_button.configure(state="disabled")
        self.wabao_button.configure(state="disabled")
        self.dati_button.configure(state="disabled")

        # 设置1秒后重新启用按钮
        self.root.after(1000, self.enable_buttons)

    def enable_buttons(self):
        """重新启用按钮"""
        self.open_button.configure(state="normal")
        self.daily_button.configure(state="normal")
        self.dungeon_task_button.configure(state="normal")
        self.button_320.configure(state="normal")
        self.ghost_button.configure(state="normal")
        self.kaogu_button.configure(state="normal")
        self.lls_button.configure(state="normal")
        self.app_path_entry.configure(state="normal")
        self.config_button.configure(state="normal")
        self.baotu_button.configure(state="normal")
        self.yabiao_button.configure(state="normal")
        self.mijing_button.configure(state="normal")
        self.wabao_button.configure(state="normal")
        self.dati_button.configure(state="normal")


if __name__ == "__main__":
    App()
