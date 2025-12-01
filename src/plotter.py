import matplotlib.pyplot as plt
from .theme import Theme
from .calculator import InterpolationCalculator

# 弗雷瑟图绘制器
class FraserPlotter:
    # 初始化绘
    def __init__(self, ax, canvas):
        self.ax = ax
        self.canvas = canvas
        self.highlight_artists = []

    # 清除图形
    def clear(self):
        self.ax.clear()
        self.clear_highlights()

    # 清除高亮路径
    def clear_highlights(self):
        for artist in self.highlight_artists:
            artist.remove()
        self.highlight_artists = []
        self.canvas.draw()

    # 绘制路径线段
    def draw_line(self, r1, c1, r2, c2, color):
        x1, y1 = c1, -(r1 + c1/2.0)
        x2, y2 = c2, -(r2 + c2/2.0)
        line, = self.ax.plot([x1, x2], [y1, y2], color=color, lw=5, alpha=0.8, zorder=10)
        self.highlight_artists.append(line)

    # 绘制弗雷瑟图
    def plot_diagram(self, calc: InterpolationCalculator):
        self.clear()
        ax = self.ax
        n = calc.n
        
        ax.set_title("FRASER DIAGRAM", fontsize=16, color=Theme.COLORS["border"], pad=15, fontname=Theme.FONT_FAMILY, weight="bold")
        ax.set_axis_off()
        font_size = 9
        
        for j in range(n):
            for i in range(n - j):
                val = calc.diff_table[i][j]
                x_pos = j
                y_pos = -(i + j/2.0)
                if j > 0:
                    prev_y_u, prev_y_l = -(i + (j-1)/2.0), -((i+1) + (j-1)/2.0)
                    ax.plot([j-1, j], [prev_y_u, y_pos], color=Theme.COLORS["border"], lw=2, ls='-', zorder=1) 
                    ax.plot([j-1, j], [prev_y_l, y_pos], color=Theme.COLORS["border"], lw=2, ls='-', zorder=1)
                ax.text(x_pos, y_pos, f"{val:.4f}", ha='center', va='center', color=Theme.COLORS["text_dark"],
                        bbox=dict(boxstyle="square,pad=0.3", fc=Theme.COLORS["paper"], ec=Theme.COLORS["border"], lw=2),
                        fontsize=font_size, fontname=Theme.FONT_FAMILY, weight="bold", zorder=20) 

        ax.axhline(y=-calc.base_k, color=Theme.COLORS["accent"], linestyle='--', linewidth=3, zorder=5)
        ax.text(n-0.5, -calc.base_k, f"BASE {calc.base_k}", color=Theme.COLORS["accent"], fontsize=font_size, va='center', fontname=Theme.FONT_FAMILY, weight="bold")
        self.canvas.figure.tight_layout()
        self.canvas.draw()

    # 高亮显示插值路径
    def highlight_path(self, method, calc: InterpolationCalculator):
        self.clear_highlights()
        k = calc.base_k
        n = calc.n
        color = Theme.PATH_COLORS.get(method, "red")
        
        # 1. 牛顿前插
        if method == "Newton F":
            for j in range(1, n):
                if k > n - 1 - j: break
                self.draw_line(k, j-1, k, j, color)

        # 2. 牛顿后插
        elif method == "Newton B":
            for j in range(1, n):
                r_prev = k - (j-1)
                r_curr = k - j
                if r_curr < 0: break
                self.draw_line(r_prev, j-1, r_curr, j, color)

        # 3. 高斯向前
        elif method == "Gauss F":
            curr_r = k
            for j in range(1, n):
                next_r = curr_r
                if j % 2 == 0: next_r = curr_r - 1
                if next_r < 0 or next_r > n - 1 - j: break
                self.draw_line(curr_r, j-1, next_r, j, color)
                curr_r = next_r

        # 4. 高斯向后
        elif method == "Gauss B":
            curr_r = k
            for j in range(1, n):
                next_r = curr_r
                if j % 2 != 0: next_r = curr_r - 1
                if next_r < 0 or next_r > n - 1 - j: break
                self.draw_line(curr_r, j-1, next_r, j, color)
                curr_r = next_r

        # 5. 斯特林
        elif method == "Stirling":
            curr_r = k
            for j in range(1, n):
                next_r = curr_r
                if j % 2 == 0: next_r = curr_r - 1
                if next_r < 0 or next_r > n - 1 - j: break
                self.draw_line(curr_r, j-1, next_r, j, color)
                curr_r = next_r
            
            curr_r = k
            for j in range(1, n):
                next_r = curr_r
                if j % 2 != 0: next_r = curr_r - 1
                if next_r < 0 or next_r > n - 1 - j: break
                self.draw_line(curr_r, j-1, next_r, j, color)
                curr_r = next_r

        # 6. 贝塞尔
        elif method == "Bessel":
            for j in range(1, n):
                m = j // 2
                if j % 2 == 1: 
                    # 奇数列 j: 目标是 (k-m, j)
                    r_target = k - m
                    if r_target < 0 or r_target > n - 1 - j: continue
                    
                    # 来源自 j-1: (k-m, j-1) 和 (k-m+1, j-1)
                    r_src1 = k - m
                    r_src2 = k - m + 1
                    
                    if 0 <= r_src1 <= n - 1 - (j-1):
                        self.draw_line(r_src1, j-1, r_target, j, color)
                    if 0 <= r_src2 <= n - 1 - (j-1):
                        self.draw_line(r_src2, j-1, r_target, j, color)
                else:
                    # 偶数列 j: 目标是 (k-m, j) 和 (k-m+1, j)
                    # 来源自 j-1: (k-m+1, j-1)
                    r_src = k - m + 1
                    if r_src < 0 or r_src > n - 1 - (j-1): continue
                        
                    r_target1 = k - m
                    if 0 <= r_target1 <= n - 1 - j:
                        self.draw_line(r_src, j-1, r_target1, j, color)
                    
                    r_target2 = k - m + 1
                    if 0 <= r_target2 <= n - 1 - j:
                        self.draw_line(r_src, j-1, r_target2, j, color)

        self.canvas.draw()
