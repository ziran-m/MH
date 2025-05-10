import importlib
import os
import sys
import customtkinter as ctk

from mh_script.constant.constant import Constant
from mh_script.utils.log_util import TextHandler, logger

class AppUI:
    def __init__(self, root):
        self.root = root
        self.root.title("脚本【version1.0】")
        self.root.geometry("700x500")  # 设置窗口大小
        self.root.config(bg="#2b2b2b")  # 设置背景色

        # 使用 Dark/Light 模式
        ctk.set_appearance_mode("dark")

        # 设置字体
        self.font_style = ("Arial", 14)

        # 创建滚动条和文本框显示日志
        self.create_log_ui()

        # 创建按钮并绑定命令
        self.create_buttons()

        # 配置行和列的自适应大小
        self.configure_grid()

    def create_log_ui(self):
        """创建日志区域（文本框和滚动条）"""
        self.scrollbar = ctk.CTkScrollbar(self.root, orientation="vertical")

        self.log_text = ctk.CTkTextbox(self.root, font=self.font_style, wrap="word", state="normal")
        self.log_text.grid(row=0, column=1, padx=20, pady=20, rowspan=3, sticky="nsew")  # 使用 grid 布局，控制文本框的高度和位置
        self.log_text.configure(yscrollcommand=self.scrollbar.set)  # 使用 'configure' 而不是 'config'
        self.scrollbar.configure(command=self.log_text.yview)

        # 创建 TextHandler 并添加到 logger
        self.log_text_handler = TextHandler(self.log_text)  # 将 UI 中的 Text 控件传入
        logger.addHandler(self.log_text_handler)  # 将 handler 添加到原始 logger

    def create_buttons(self):
        """创建操作按钮"""
        # 启动按钮
        self.open_button = ctk.CTkButton(self.root, text="启动", font=self.font_style, height=40, width=200,
                                         corner_radius=10, fg_color="#1e1e1e", hover_color="#3a3a3a", command=self.start_task)
        self.open_button.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        # 日常按钮
        self.daily_button = ctk.CTkButton(self.root, text="日常", font=self.font_style, height=40, width=200,
                                          corner_radius=10, fg_color="#1e1e1e", hover_color="#3a3a3a", command=self.daily_task)
        self.daily_button.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        # 副本按钮
        self.dungeon_task_button = ctk.CTkButton(self.root, text="副本", font=self.font_style, height=40, width=200,
                                          corner_radius=10, fg_color="#1e1e1e", hover_color="#3a3a3a", command=self.dungeon_task_task)
        self.dungeon_task_button.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

        # 抓鬼按钮
        self.ghost_button = ctk.CTkButton(self.root, text="抓鬼", font=self.font_style, height=40, width=200,
                                                 corner_radius=10, fg_color="#1e1e1e", hover_color="#3a3a3a",
                                                 command=self.ghost_task)
        self.ghost_button.grid(row=3, column=0, padx=20, pady=20, sticky="ew")

        # 名称为 320 的按钮
        self.button_320 = ctk.CTkButton(self.root, text="320", font=self.font_style, height=40, width=200,
                                        corner_radius=10, fg_color="#1e1e1e", hover_color="#3a3a3a",
                                        command=self.task_320)
        self.button_320.grid(row=4, column=0, padx=20, pady=20, sticky="ew")

        # 副本轮数输入框
        self.dungeon_num_entry = ctk.CTkEntry(self.root, placeholder_text="副本开始点 0 侠士 1 普本1 2 普本2", font=self.font_style, width=200)
        self.dungeon_num_entry.grid(row=5, column=0, padx=20, pady=(0, 10), sticky="ew")

        # 抓鬼轮数输入框
        self.ghost_num_entry = ctk.CTkEntry(self.root, placeholder_text="抓鬼轮数 (默认2)", font=self.font_style, width=200)
        self.ghost_num_entry.grid(row=6, column=0, padx=20, pady=(0, 20), sticky="ew")


    def configure_grid(self):
        """配置行和列的自适应大小"""
        self.root.grid_rowconfigure(0, weight=1)  # 第一行（按钮行）自适应
        self.root.grid_rowconfigure(1, weight=1)  # 第二行（按钮行）自适应
        self.root.grid_rowconfigure(2, weight=1)  # 第三行（按钮行）自适应
        self.root.grid_rowconfigure(3, weight=3)  # 第四行（日志显示区域）占更多空间

        self.root.grid_columnconfigure(0, weight=1)  # 第一列（按钮列）自适应
        self.root.grid_columnconfigure(1, weight=3)  # 第二列（日志列）占更多空间

    def execute_file(self, file_name):
        """加载并执行指定文件的 main 方法"""
        try:

            # 动态加载模块
            module = importlib.import_module(f"{file_name}")

            # 调用模块中的 main 方法
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
        self.execute_file("daily_task")

    def dungeon_task_task(self):
        """副本任务（对应 '关闭' 按钮）"""
        self.disable_buttons_temporarily()  # 禁用按钮
        try:
            val = int(self.dungeon_num_entry.get().strip())
        except ValueError:
            val = 0

        Constant.DUNGEON_NUM = val
        logger.info(f"副本轮数设置为：{Constant.DUNGEON_NUM}")

        self.execute_file("dungeon_task")

    def ghost_task(self):
        """关闭任务（对应 '关闭' 按钮）"""
        self.disable_buttons_temporarily()  # 禁用按钮

        try:
            val = int(self.ghost_num_entry.get().strip())
        except ValueError:
            val = 2

        Constant.GHOST_NUM = val
        logger.info(f"抓鬼轮数设置为：{Constant.GHOST_NUM}")

        self.execute_file("ghost_task")

    def task_320(self):
        """320任务（对应 '320' 按钮）"""
        self.disable_buttons_temporarily()  # 禁用按钮
        self.execute_file("three_two_zero")

    def disable_buttons_temporarily(self):
        """禁用按钮并在1秒后重新启用"""
        self.open_button.configure(state="disabled")
        self.daily_button.configure(state="disabled")
        self.dungeon_task_button.configure(state="disabled")
        self.button_320.configure(state="disabled")
        self.ghost_button.configure(state="disabled")

        # 设置1秒后重新启用按钮
        self.root.after(1000, self.enable_buttons)

    def enable_buttons(self):
        """重新启用按钮"""
        self.open_button.configure(state="normal")
        self.daily_button.configure(state="normal")
        self.dungeon_task_button.configure(state="normal")
        self.button_320.configure(state="normal")
        self.ghost_button.configure(state="normal")


def main():
    # 创建UI窗口
    app = ctk.CTk()
    # 创建AppUI实例
    ui = AppUI(app)

    # 启动UI主循环
    app.mainloop()


if __name__ == "__main__":
    main()
