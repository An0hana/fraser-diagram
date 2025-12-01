import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from .theme import Theme

class CurvePlotter:
    def __init__(self, master_window):
        self.master = master_window
        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.fig.patch.set_facecolor(Theme.COLORS["paper"])
        self.ax.set_facecolor(Theme.COLORS["paper"])
        self.fig.subplots_adjust(left=0.12, right=0.95, top=0.92, bottom=0.12)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def plot(self, calculator, true_func_str=None, method_name=None):
        self.ax.clear()
        
        # 1. 获取数据范围
        if calculator.X is None: return

        x_min, x_max = calculator.X[0], calculator.X[-1]
        padding = (x_max - x_min) * 0.1
        x_range = np.linspace(x_min - padding, x_max + padding, 200)
        
        # 2. 计算插值多项式 P(x)
        if method_name:
            y_interp = [calculator.calculate_method_value(method_name, x) for x in x_range]
            label_text = f"{method_name} P(x)"
            color = Theme.PATH_COLORS.get(method_name, "red")
        else:
            y_interp = [calculator.get_interpolated_value(x) for x in x_range]
            label_text = "Global Poly P(x)"
            color = "red"
        
        # 3. 绘制真实函数 (如果提供)
        if true_func_str:
            try:
                # 创建安全的求值环境
                safe_dict = {"x": x_range, "np": np, "sin": np.sin, "cos": np.cos, "exp": np.exp, "log": np.log, "sqrt": np.sqrt, "pow": np.power}
                y_true = eval(true_func_str, {"__builtins__": None}, safe_dict)
                
                self.ax.plot(x_range, y_true, color="green", linewidth=2, alpha=0.6, label="True f(x)")
            except Exception as e:
                print(f"Error plotting true function: {e}")

        # 4. 绘制插值曲线
        self.ax.plot(x_range, y_interp, color=color, linestyle="--", linewidth=1.5, label=label_text)
        
        # 5. 绘制原始数据点
        self.ax.scatter(calculator.X, calculator.Y, color="blue", s=30, zorder=5, label="Data")
        
        # 设置图表样式
        self.ax.set_title("Curve Comparison", fontsize=10, pad=5, fontname=Theme.FONT_FAMILY, weight="bold")
        self.ax.tick_params(axis='both', which='major', labelsize=8)
        self.ax.grid(True, linestyle='--', alpha=0.5)
        self.ax.legend(fontsize=8)
        
        self.canvas.draw()
