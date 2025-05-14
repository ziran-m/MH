import customtkinter as ctk


class App:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("400x300")

        # 添加一个属性来保存弹框的引用
        self.config_win = None

        # 创建按钮，点击时弹出配置对话框
        self.button = ctk.CTkButton(self.root, text="打开配置框", command=self.open_config_window)
        self.button.place(relx=0.5, rely=0.5, anchor="center")

    def open_config_window(self):
        # 如果弹框已经打开，则不再创建新的弹框
        if self.config_win is not None and self.config_win.winfo_exists():
            return  # 如果弹框存在且未关闭，则不再打开新的弹框

        # 创建一个顶级弹框窗口
        self.config_win = ctk.CTkToplevel(self.root)
        self.config_win.title("配置窗口")
        self.config_win.geometry("400x300")

        # 将弹框设置为最上层
        self.config_win.attributes("-topmost", True)

        # 创建标签和文本框
        label1 = ctk.CTkLabel(self.config_win, text="请输入第一个数字:")
        label1.pack(pady=(20, 5))

        entry1 = ctk.CTkEntry(self.config_win)
        entry1.pack(pady=5)

        label2 = ctk.CTkLabel(self.config_win, text="请输入第二个数字:")
        label2.pack(pady=5)

        entry2 = ctk.CTkEntry(self.config_win)
        entry2.pack(pady=5)

        # 创建保存按钮
        def save_config():
            num1 = entry1.get()
            num2 = entry2.get()
            print(f"第一个数字: {num1}, 第二个数字: {num2}")
            self.config_win.destroy()
            self.config_win = None  # 重置弹框引用，允许再次打开

        save_button = ctk.CTkButton(self.config_win, text="保存", command=save_config)
        save_button.pack(pady=10)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
