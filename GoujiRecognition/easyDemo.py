import tkinter as tk
from tkinter import font as tkfont


class CardCounter:
    def __init__(self, root):
        self.root = root
        self.root.title("记牌器")
        self.root.geometry("500x900")  # 增大窗口尺寸
        self.root.resizable(False, False)

        # 设置窗口图标
        self.root.iconbitmap("")  # 你可以添加一个ico文件

        # 设置字体 - 增大字体尺寸
        self.title_font = tkfont.Font(family="SimHei", size=24, weight="bold")
        self.card_font = tkfont.Font(family="SimHei", size=20)
        self.button_font = tkfont.Font(family="SimHei", size=16)

        # 初始化牌的数量
        self.big_joker_count = 4
        self.small_joker_count = 4
        self.two_count = 16

        # 创建框架
        self.create_frames()

        # 创建界面元素
        self.create_widgets()

        # 更新显示
        self.update_display()

        # 绑定关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_frames(self):
        # 创建标题框架
        self.title_frame = tk.Frame(self.root, pady=15)
        self.title_frame.pack(fill=tk.X)

        # 创建牌显示框架
        self.cards_frame = tk.Frame(self.root, pady=15)
        self.cards_frame.pack(fill=tk.X)

        # 创建按钮框架
        self.buttons_frame = tk.Frame(self.root, pady=25)
        self.buttons_frame.pack(fill=tk.BOTH, expand=True)

        # 创建底部框架
        self.bottom_frame = tk.Frame(self.root, pady=15)
        self.bottom_frame.pack(fill=tk.X, side=tk.BOTTOM)

    def create_widgets(self):
        # 标题
        tk.Label(self.title_frame, text="记牌器", font=self.title_font).pack()

        # 牌的显示
        self.big_joker_label = tk.Label(self.cards_frame, text="", font=self.card_font)
        self.big_joker_label.pack(pady=8)

        self.small_joker_label = tk.Label(
            self.cards_frame, text="", font=self.card_font
        )
        self.small_joker_label.pack(pady=8)

        self.two_label = tk.Label(self.cards_frame, text="", font=self.card_font)
        self.two_label.pack(pady=8)

        # 为三种牌创建三列按钮
        # 使用Grid布局来排列按钮
        column_frame = tk.Frame(self.buttons_frame)
        column_frame.pack(expand=True)

        # 大王列
        big_joker_frame = tk.Frame(column_frame, padx=20)
        big_joker_frame.grid(row=0, column=0, padx=25)

        tk.Label(big_joker_frame, text="大王", font=self.card_font).pack(pady=10)

        for i in range(1, 5):  # 1到4的按钮
            tk.Button(
                big_joker_frame,
                text=str(i),
                width=4,
                height=2,
                font=self.button_font,
                command=lambda i=i, card="大王": self.decrease_count(card, i),
            ).pack(pady=10)

        # 小王列
        small_joker_frame = tk.Frame(column_frame, padx=20)
        small_joker_frame.grid(row=0, column=1, padx=25)

        tk.Label(small_joker_frame, text="小王", font=self.card_font).pack(pady=10)

        for i in range(1, 5):  # 1到4的按钮
            tk.Button(
                small_joker_frame,
                text=str(i),
                width=4,
                height=2,
                font=self.button_font,
                command=lambda i=i, card="小王": self.decrease_count(card, i),
            ).pack(pady=10)

        # 2列
        two_frame = tk.Frame(column_frame, padx=20)
        two_frame.grid(row=0, column=2, padx=25)

        tk.Label(two_frame, text="2", font=self.card_font).pack(pady=10)

        for i in range(1, 7):  # 1到6的按钮
            tk.Button(
                two_frame,
                text=str(i),
                width=4,
                height=2,
                font=self.button_font,
                command=lambda i=i, card="2": self.decrease_count(card, i),
            ).pack(pady=5)

        # 重置按钮
        reset_frame = tk.Frame(self.bottom_frame)
        reset_frame.pack()

        tk.Button(
            reset_frame,
            text="重置",
            font=self.button_font,
            width=10,
            height=2,
            command=self.reset_counts,
        ).pack(pady=10)

    def update_display(self):
        self.big_joker_label.config(text=f"大王: {self.big_joker_count}张")
        self.small_joker_label.config(text=f"小王: {self.small_joker_count}张")
        self.two_label.config(text=f"2: {self.two_count}张")

    def decrease_count(self, card, amount):
        if card == "大王":
            self.big_joker_count = max(0, self.big_joker_count - amount)
        elif card == "小王":
            self.small_joker_count = max(0, self.small_joker_count - amount)
        elif card == "2":
            self.two_count = max(0, self.two_count - amount)

        self.update_display()

    def reset_counts(self):
        self.big_joker_count = 4
        self.small_joker_count = 4
        self.two_count = 16
        self.update_display()

    def on_closing(self):
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = CardCounter(root)
    root.mainloop()
