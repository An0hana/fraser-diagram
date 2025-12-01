import tkinter as tk
from tkinter import ttk, messagebox
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from .theme import Theme
from .plotter import FraserPlotter
from .curve_plotter import CurvePlotter
from .logger import LogHandler
from .calculator import InterpolationCalculator

# 主应用类
class InterpolationApp:
    # 初始化
    def __init__(self, root):
        self.root = root
        self.root.title("Fraser diagram") 
        self.root.geometry("1300x850") 
        self.root.configure(bg=Theme.COLORS["bg_wood"]) 

        # 设置程序图标
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            icon_png = os.path.join(base_dir, "assets", "icon.png")
            if os.path.exists(icon_png):
                img = tk.PhotoImage(file=icon_png)
                self.root.iconphoto(True, img)
        except Exception:
            pass

        Theme.apply_styles()
        
        self.calculator = InterpolationCalculator()
        self.plotter = None
        self.logger = None
        
        self.setup_ui()

    # 设置用户界面
    def setup_ui(self):
        main_container = ttk.Frame(self.root, padding=20)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # 数据输入 
        input_frame = ttk.LabelFrame(main_container, text=" DATA ENTRY ", padding=20)
        input_frame.pack(fill="x", pady=(0, 20))
        input_frame.columnconfigure(0, weight=0)
        input_frame.columnconfigure(1, weight=1) 
        input_frame.columnconfigure(2, weight=0)

        ttk.Label(input_frame, text="X NODES:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_x = ttk.Entry(input_frame)
        self.entry_x.grid(row=0, column=1, sticky="ew", padx=15, pady=5)
        self.entry_x.insert(0, "0, 1, 2, 3, 4, 5")

        ttk.Label(input_frame, text="Y VALUES:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_y = ttk.Entry(input_frame)
        self.entry_y.grid(row=1, column=1, sticky="ew", padx=15, pady=5)
        self.entry_y.insert(0, "1.0, 1.5, 2.2, 3.1, 4.6, 6.5")

        ttk.Label(input_frame, text="TARGET X:").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_target = ttk.Entry(input_frame)
        self.entry_target.grid(row=2, column=1, sticky="ew", padx=15, pady=5)
        self.entry_target.insert(0, "2.5")

        ttk.Label(input_frame, text="TRUE FUNC:").grid(row=3, column=0, sticky="w", pady=5)
        self.entry_func = ttk.Entry(input_frame)
        self.entry_func.grid(row=3, column=1, sticky="ew", padx=15, pady=5)
        self.entry_func.insert(0, "x**3") # Default example

        self.btn_calc = ttk.Button(input_frame, text="CRAFT!", command=self.process_data, cursor="hand2")
        self.btn_calc.grid(row=0, column=2, rowspan=4, sticky="nsew", padx=(10, 0), pady=5)

        # 内容区域
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill="both", expand=True)

        # 地图区域
        plot_frame = ttk.LabelFrame(content_frame, text=" MAP ", padding=5)
        plot_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))

        self.fig, self.ax = plt.subplots(figsize=(6, 6), dpi=100)
        self.fig.patch.set_facecolor(Theme.COLORS["paper"])
        self.ax.set_facecolor(Theme.COLORS["paper"])
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.canvas.get_tk_widget().configure(bg=Theme.COLORS["border"], highlightthickness=3, highlightbackground=Theme.COLORS["border"])
        
        self.plotter = FraserPlotter(self.ax, self.canvas)

        # 右侧面板
        right_panel = ttk.Frame(content_frame, width=450)
        right_panel.pack(side="right", fill="y")

        # 账本
        summary_frame = ttk.LabelFrame(right_panel, text=" LEDGER ", padding=5)
        summary_frame.pack(fill="x", pady=(0, 15))
        
        cols = ("method", "result")
        self.tree = ttk.Treeview(summary_frame, columns=cols, show="headings", height=8)
        self.tree.heading("method", text="METHOD")
        self.tree.heading("result", text="VALUE")
        self.tree.column("method", width=160, anchor="center") 
        self.tree.column("result", width=160, anchor="center")
        self.tree.pack(fill="x")
        
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Button-1>", self.disable_resize)

        # 分析区域
        analysis_frame = ttk.LabelFrame(right_panel, text=" ANALYSIS ", padding=5)
        analysis_frame.pack(fill="both", expand=True, pady=(0, 15))

        self.curve_frame = ttk.Frame(analysis_frame)
        self.curve_frame.pack(fill="both", expand=True)
        
        self.curve_plotter = CurvePlotter(self.curve_frame)

        # 日志区域
        log_frame = ttk.LabelFrame(right_panel, text=" LOG ", padding=5)
        log_frame.pack(fill="x", pady=(0, 0))

        text_out = tk.Text(log_frame, 
                                height=12,
                                font=(Theme.FONT_FAMILY, 10), 
                                bg=Theme.COLORS["paper"], 
                                fg=Theme.COLORS["text_dark"], 
                                relief="flat",
                                bd=0,
                                highlightthickness=0)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=text_out.yview)
        text_out.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        text_out.pack(fill="both", expand=True)

        text_out.tag_config("title", font=(Theme.FONT_FAMILY, 11, "bold"), foreground=Theme.COLORS["border"])
        text_out.tag_config("accent", foreground=Theme.COLORS["accent"], font=(Theme.FONT_FAMILY, 10, "bold"))
        text_out.tag_config("info", foreground=Theme.COLORS["info"])
        text_out.tag_config("warn", foreground=Theme.COLORS["warn"])
        
        self.logger = LogHandler(text_out)

    # 禁止调列宽
    def disable_resize(self, event):
        if self.tree.identify_region(event.x, event.y) == "separator":
            return "break"

    # 行选择事件
    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if not selected_item: return
        
        item = self.tree.item(selected_item)
        method_name = item['values'][0]
        
        if method_name in Theme.PATH_COLORS:
            self.plotter.highlight_path(method_name, self.calculator)
            
            # Update curve with selected method
            true_func = self.entry_func.get().strip()
            self.curve_plotter.plot(self.calculator, true_func if true_func else None, method_name)
        else:
            self.plotter.clear_highlights()
            # Reset curve to default
            true_func = self.entry_func.get().strip()
            self.curve_plotter.plot(self.calculator, true_func if true_func else None)

    # 处理数据
    def process_data(self):
        self.logger.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.plotter.clear()

        try:
            self.calculator.load_data(
                self.entry_x.get(),
                self.entry_y.get(),
                self.entry_target.get()
            )
            
            self.plotter.plot_diagram(self.calculator)
            results = self.calculator.calculate_all()

            # Initial plot (default)
            true_func = self.entry_func.get().strip()
            self.curve_plotter.plot(self.calculator, true_func if true_func else None)

            # 显示结果
            values_list = []
            for m_name, val in results.items():
                self.tree.insert("", "end", values=(m_name, f"{val:.6f}"))
                values_list.append(val)
            
            avg_val = np.mean(values_list)
            self.tree.insert("", "end", values=("-------", "-------"), tags=('separator_row',))
            self.tree.insert("", "end", values=("AVERAGE", f"{avg_val:.6f}"), tags=('total_row',))

            # 日志报告
            #self.logger.tag("📜EXPERIMENT REPORT", "title")
            #self.logger.separator()
            self.logger.tag("[1] ITEM INSPECTION", "title")
            self.logger.plain(f"• Step Size (h): {self.calculator.h}")
            self.logger.plain(f"• Base Node (x0): {self.calculator.X[self.calculator.base_k]}")
            p = self.calculator.p
            p_desc = "Center" if abs(p) < 0.1 else ("Right" if p > 0 else "Left")
            self.logger.plain(f"• Position (p): {p:.3f} ({p_desc})")
            
            self.logger.separator()
            self.logger.tag("[2] STABILITY CHECK", "title")
            rng = max(values_list) - min(values_list)
            if rng < 1e-5:
                self.logger.tag("High Precision", "info")
            elif rng < 0.1:
                self.logger.tag("Minor Fluctuations", "accent")
            else:
                self.logger.tag("Unstable Results", "warn")
            
            self.logger.separator()
            self.logger.tag("[3] INTERACTION", "title")
            self.logger.tag("👉 Click LEDGER rows to see paths!", "accent")

        except Exception as e:
            messagebox.showerror("Broken Tool", str(e))


