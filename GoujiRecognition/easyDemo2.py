import tkinter as tk
from tkinter import font as tkfont


class CardCounter:
    def __init__(self, root):
        self.root = root
        self.root.title("记牌器")
        self.root.geometry("950x280")  # 进一步减小高度
        self.root.resizable(False, False)

        # 设置窗口图标
        self.root.iconbitmap("")  # 你可以添加一个ico文件

        # 设置字体
        self.card_font = tkfont.Font(family="SimHei", size=20)
        self.button_font = tkfont.Font(family="SimHei", size=16)

        # 初始化牌的数量
        self.big_joker_count = 4
        self.small_joker_count = 4
        self.two_count = 16

        # 创建主框架
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 创建左侧和右侧框架
        self.left_frame = tk.Frame(self.main_frame, width=300, padx=30, pady=20)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        self.right_frame = tk.Frame(self.main_frame, padx=20, pady=15)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 创建界面元素
        self.create_widgets()

        # 更新显示
        self.update_display()

        # 绑定关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # 剩余牌的数量显示 (竖向排列)
        self.big_joker_label = tk.Label(
            self.left_frame, text="", font=self.card_font, anchor="w", width=15
        )
        self.big_joker_label.pack(pady=10, anchor="w")

        self.small_joker_label = tk.Label(
            self.left_frame, text="", font=self.card_font, anchor="w", width=15
        )
        self.small_joker_label.pack(pady=10, anchor="w")

        self.two_label = tk.Label(
            self.left_frame, text="", font=self.card_font, anchor="w", width=15
        )
        self.two_label.pack(pady=10, anchor="w")

        # 重置按钮
        tk.Button(
            self.left_frame,
            text="重置",
            font=self.button_font,
            width=10,
            height=2,
            command=self.reset_counts,
        ).pack(pady=(20, 0))

        # 右侧按钮区域 - 使用网格布局
        # 大王行
        tk.Label(self.right_frame, text="大王", font=self.card_font, width=4).grid(
            row=0, column=0, padx=(0, 10), pady=15
        )

        for i in range(1, 5):
            tk.Button(
                self.right_frame,
                text=str(i),
                width=5,
                height=2,
                font=self.button_font,
                command=lambda i=i, card="大王": self.decrease_count(card, i),
            ).grid(row=0, column=i, padx=8)

        # 小王行
        tk.Label(self.right_frame, text="小王", font=self.card_font, width=4).grid(
            row=1, column=0, padx=(0, 10), pady=15
        )

        for i in range(1, 5):
            tk.Button(
                self.right_frame,
                text=str(i),
                width=5,
                height=2,
                font=self.button_font,
                command=lambda i=i, card="小王": self.decrease_count(card, i),
            ).grid(row=1, column=i, padx=8)

        # 2行
        tk.Label(self.right_frame, text="2", font=self.card_font, width=4).grid(
            row=2, column=0, padx=(0, 10), pady=15
        )

        for i in range(1, 7):
            tk.Button(
                self.right_frame,
                text=str(i),
                width=5,
                height=2,
                font=self.button_font,
                command=lambda i=i, card="2": self.decrease_count(card, i),
            ).grid(row=2, column=i, padx=5)

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
