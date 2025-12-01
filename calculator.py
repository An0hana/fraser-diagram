import numpy as np
import math

# 插值计算器类
class InterpolationCalculator:
    # 初始化
    def __init__(self):
        self.reset()

    # 重置数据
    def reset(self):
        self.X = None
        self.Y = None
        self.diff_table = None
        self.h = None
        self.target_x = None
        self.base_k = None
        self.p = None
        self.n = 0

    # 加载数据
    def load_data(self, x_str, y_str, target_str):
        if not target_str: raise ValueError("Target X is empty")
        self.target_x = float(target_str)

        x_arr = np.array([float(x) for x in x_str.replace('，', ',').split(',')])
        y_arr = np.array([float(y) for y in y_str.replace('，', ',').split(',')])

        if len(x_arr) != len(y_arr): raise ValueError("Mismatch Len")
        diff = np.diff(x_arr)
        if not np.allclose(diff, diff[0]): raise ValueError("Not Equal Dist")

        self.X = x_arr
        self.Y = y_arr
        self.h = diff[0]
        self.n = len(self.X)
        self.base_k = int(np.abs(self.X - self.target_x).argmin())
        self.p = (self.target_x - self.X[self.base_k]) / self.h
        
        self._build_diff_table()

    # 构建差分表
    def _build_diff_table(self):
        self.diff_table = np.zeros((self.n, self.n))
        self.diff_table[:, 0] = self.Y
        for j in range(1, self.n):
            for i in range(self.n - j):
                self.diff_table[i][j] = self.diff_table[i+1][j-1] - self.diff_table[i][j-1]

    # 计算二项式系数
    def binom(self, n, k):
        if k < 0: return 0
        if k == 0: return 1.0
        res = 1.0
        for i in range(k): res = res * (n - i)
        return res / math.factorial(k)

    def get_diff(self, row, order):
        if row < 0 or row >= self.n or row > self.n - 1 - order: return 0.0
        return self.diff_table[row][order]

    # 计算任意点的插值多项式值 (使用牛顿前插公式从x0开始)
    def get_interpolated_value(self, x):
        if self.X is None or self.n == 0:
            return 0
        
        # p = (x - x0) / h
        p = (x - self.X[0]) / self.h
        
        val = 0
        # P(x) = sum( binom(p, j) * diff_table[0][j] )
        for j in range(self.n):
            term = self.binom(p, j) * self.diff_table[0][j]
            val += term
            
        return val

    def calculate_all(self):
        p, k, n = self.p, self.base_k, self.n
        results = {}
        
        # 牛顿前插
        val = sum(self.binom(p, j) * self.get_diff(k, j) for j in range(n) if k <= n-1-j)
        results['Newton F'] = val
        
        # 牛顿后插
        val = sum(self.binom(p + j - 1, j) * self.get_diff(k - j, j) for j in range(n) if k - j >= 0)
        results['Newton B'] = val
        
        # 3. 高斯向前
        val = 0
        for j in range(n):
            row = k - (j // 2)
            m = j // 2
            coef = self.binom(p + m - 1, j) if (j > 0 and j % 2 == 0) else self.binom(p + m, j)
            val += coef * self.get_diff(row, j)
        results['Gauss F'] = val
        
        # 4. 高斯向后
        val = 0
        for j in range(n):
            row = k - ((j + 1) // 2)
            m = j // 2
            coef = self.binom(p + m, j)
            val += coef * self.get_diff(row, j)
        results['Gauss B'] = val
        
        # 5. 斯特林
        results['Stirling'] = (results['Gauss F'] + results['Gauss B']) / 2
        
        # 6. 贝塞尔
        val_bessel = 0
        for m in range(n // 2 + 1):
            j2 = 2 * m
            if j2 < n:
                coef = 1 if m == 0 else self.binom(p + m - 1, j2)
                mean_diff = (self.get_diff(k-m, j2) + self.get_diff(k-m+1, j2))/2
                val_bessel += coef * mean_diff
            j3 = 2 * m + 1
            if j3 < n:
                coef = (1 if m == 0 else self.binom(p + m - 1, 2*m)) * (p-0.5)/(2*m+1)
                val_bessel += coef * self.get_diff(k-m, j3)
        results['Bessel'] = val_bessel
        
        return results
