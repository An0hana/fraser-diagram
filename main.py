import sys
import os
import tkinter as tk
import ctypes
import matplotlib.pyplot as plt

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.app import InterpolationApp

# 基础设置
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

# 任务栏显示图标
try:
    myappid = 'anohana.fraser_diagram.app.2.0' 
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except:
    pass

plt.rcParams['font.family'] = 'monospace' 
plt.rcParams['font.monospace'] = ['Courier New', 'Consolas'] 
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['text.antialiased'] = True 
plt.rcParams['lines.antialiased'] = True

# 启动应用
if __name__ == "__main__":
    root = tk.Tk()
    app = InterpolationApp(root)
    root.mainloop()
