import tkinter as tk

# 日志处理
class LogHandler:
    # 初始化
    def __init__(self, text_widget):
        self.text_out = text_widget
        self.text_out.configure(state="disabled")

    # 内部写入方法
    def _write(self, msg, tag=None):
        self.text_out.configure(state="normal")
        if tag:
            self.text_out.insert("end", msg + "\n", tag)
        else:
            self.text_out.insert("end", msg + "\n")
        self.text_out.see("end")
        self.text_out.configure(state="disabled")

    # 普通日志
    def plain(self, msg):
        self._write(msg)

    # 带标签日志
    def tag(self, msg, tag):
        self._write(msg, tag)

    # 分隔线
    def separator(self):
        self._write("-" * 30)

    # 清空日志
    def clear(self):
        self.text_out.configure(state="normal")
        self.text_out.delete(1.0, "end")
        self.text_out.configure(state="disabled")
