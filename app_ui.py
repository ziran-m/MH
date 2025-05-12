import importlib
import os
import sys

import customtkinter as ctk

from mh_script.constant.constant import Constant
from mh_script.utils.log_util import TextHandler, logger, global_log


class App:
    def __init__(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.root = ctk.CTk()
        self.root.geometry("700x500")
        self.root.title("脚本启动器[当前只支持2k显示器]")

        self.font_style = ("Microsoft YaHei", 14)

        self.setup_layout()
        self.create_buttons()
        self.create_log_ui()

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

    def create_buttons(self):
        button_config = {
            "font": self.font_style,
            "height": 40,
            "width": 100,
            "corner_radius": 10,
            "fg_color": "#1abc9c",
            "hover_color": "#2A6E84",
            "text_color": "white"

        }
        # 创建一个复制的字典，并覆盖颜色配置
        exit_button_config = button_config.copy()
        exit_button_config.update({
            "fg_color": "#e74c3c",
            "hover_color": "#660000",
            "text_color": "white"
        })

        row = 0
        self.open_button = ctk.CTkButton(self.left_frame, text="启动", command=self.start_task, **button_config)
        self.open_button.grid(row=row, column=0, columnspan=2, pady=(0, 10), sticky="ew")

        row += 1
        self.dungeon_task_button = ctk.CTkButton(self.left_frame, text="副本", command=self.dungeon_task_task,
                                                 **button_config)
        self.dungeon_task_button.grid(row=row, column=0, pady=(0, 10), sticky="ew")

        # 副本输入框放在副本按钮旁边
        self.dungeon_num_entry = ctk.CTkEntry(self.left_frame, placeholder_text="副本开始点 0 侠士 1 普本1 2 普本2",
                                              font=self.font_style, width=150, height=40,border_color="#95a5a6", border_width=2)
        self.dungeon_num_entry.grid(row=row, column=1, padx=10, pady=(0, 10), sticky="ew")


        row += 1
        # 日常按钮跨越两列
        self.daily_button = ctk.CTkButton(self.left_frame, text="日常", command=self.daily_task, **button_config)
        self.daily_button.grid(row=row, column=0, columnspan=2, pady=(0, 10), sticky="ew")

        row += 1
        self.ghost_button = ctk.CTkButton(self.left_frame, text="抓鬼", command=self.ghost_task, **button_config)
        self.ghost_button.grid(row=row, column=0, pady=(0, 10), sticky="ew")

        # 抓鬼轮数输入框放在抓鬼按钮旁边
        self.ghost_num_entry = ctk.CTkEntry(self.left_frame, placeholder_text="抓鬼轮数 (默认2)", font=self.font_style,
                                            width=150, height=40,border_color="#95a5a6", border_width=2)
        self.ghost_num_entry.grid(row=row, column=1, padx=10, pady=(0, 10), sticky="ew")

        row += 1
        self.button_320 = ctk.CTkButton(self.left_frame, text="320", command=self.task_320, **button_config)
        self.button_320.grid(row=row, column=0, columnspan=2, pady=(0, 10), sticky="ew")

        row += 1
        self.wabao_button = ctk.CTkButton(self.left_frame, text="挖宝", command=self.wabao_task, **button_config)
        self.wabao_button.grid(row=row, column=0, columnspan=2, pady=(0, 10), sticky="ew")

        # 添加退出按钮到 left_frame（假设 row 是从上往下排的）

        self.exit_button = ctk.CTkButton(self.left_frame, text="退出", command=self.root.quit,**exit_button_config)
        self.exit_button.grid(row=99, column=0, columnspan=2, pady=(0, 10), sticky="ew")

        # 使按钮和输入框宽度一致
        self.left_frame.grid_columnconfigure(0, weight=1)  # 使按钮的列宽度可伸缩
        self.left_frame.grid_columnconfigure(1, weight=1)  # 使输入框的列宽度可伸缩

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

    def execute_file(self, file_name):
        """加载并执行指定文件的 main 方法"""
        try:
            # 确保当前路径下的 module 文件夹在 sys.path 中
            module_path = os.path.join(os.path.dirname(__file__), 'module')
            if module_path not in sys.path:
                sys.path.insert(0, module_path)

            # 加载模块
            module = importlib.import_module(file_name)

            # 执行 main
            if hasattr(module, 'main'):
                module.main()
            else:
                logger.error(f"模块 {file_name} 中没有找到 'main' 方法")
        except Exception as e:
            logger.error(f"执行 {file_name} 时出错: {e}")

    def start_task(self):
        """启动任务（对应 '启动' 按钮）"""
        self.disable_buttons_temporarily()  # 禁用按钮

        self.execute_file("start")

    def daily_task(self):
        """日常任务（对应 '日常' 按钮）"""
        self.disable_buttons_temporarily()  # 禁用按钮
        self.execute_file("daily")

    def dungeon_task_task(self):
        """副本任务（对应 '关闭' 按钮）"""
        self.disable_buttons_temporarily()  # 禁用按钮
        try:
            val = int(self.dungeon_num_entry.get().strip())
        except ValueError:
            val = 0

        Constant.DUNGEON_NUM = val
        global_log.info(f"副本轮数设置为：{Constant.DUNGEON_NUM}")

        self.execute_file("dungeon")

    def ghost_task(self):
        """关闭任务（对应 '关闭' 按钮）"""
        self.disable_buttons_temporarily()  # 禁用按钮

        try:
            val = int(self.ghost_num_entry.get().strip())
        except ValueError:
            val = 2

        Constant.GHOST_NUM = val
        logger.info(f"抓鬼轮数设置为：{Constant.GHOST_NUM}")

        self.execute_file("ghost")

    def task_320(self):
        """320任务（对应 '320' 按钮）"""
        self.disable_buttons_temporarily()  # 禁用按钮

        try:
            val1 = int(self.dungeon_num_entry.get().strip())
        except ValueError:
            val1 = 0

        try:
            val2 = int(self.ghost_num_entry.get().strip())
        except ValueError:
            val2 = 2

        Constant.DUNGEON_NUM = val1

        Constant.GHOST_NUM = val2

        global_log.info(f"副本轮数设置为：{Constant.DUNGEON_NUM}")

        self.execute_file("three_two_zero")

    def wabao_task(self):
        """挖宝任务"""
        self.disable_buttons_temporarily()
        self.execute_file("wabao")

    def disable_buttons_temporarily(self):
        """禁用按钮并在1秒后重新启用"""
        self.open_button.configure(state="disabled")
        self.daily_button.configure(state="disabled")
        self.dungeon_task_button.configure(state="disabled")
        self.button_320.configure(state="disabled")
        self.ghost_button.configure(state="disabled")
        self.wabao_button.configure(state="disabled")

        # 设置1秒后重新启用按钮
        self.root.after(1000, self.enable_buttons)

    def enable_buttons(self):
        """重新启用按钮"""
        self.open_button.configure(state="normal")
        self.daily_button.configure(state="normal")
        self.dungeon_task_button.configure(state="normal")
        self.button_320.configure(state="normal")
        self.ghost_button.configure(state="normal")
        self.wabao_button.configure(state="normal")


if __name__ == "__main__":
    App()
