# 弗雷瑟图表等距节点插值


> 数值分析教学演示工具。

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange?style=flat-square)
![Matplotlib](https://img.shields.io/badge/Plotting-Matplotlib-green?style=flat-square)

用于演示**有限差分**和**插值算法**。结合弗雷瑟图表和多种插值公式，帮助直观地理解数值计算过程。

## 功能

*   **交互式弗雷瑟图**：
    *   自动生成菱形差分表。
    *   **路径高亮**：点击结果表格中的方法，左侧图表自动画出该方法在差分表中的计算路径。
*   **六种插值算法**：
    *   Newton Forward / Backward (牛顿前向/后向)
    *   Gauss Forward / Backward (高斯前向/后向)
    *   Stirling (斯特林公式)
    *   Bessel (贝塞尔公式)
*   **实验报告**：
    *   自动分析步长 $h$ 和位置参数 $p$。
    *   计算结果的极差与收敛性分析。
    *   推荐最适合当前数据的插值方法。
*   **结果**：清晰展示各方法计算结果及平均值。

## 运行

### 1. 环境要求
安装 **Python 3.8+**。

### 2. 克隆仓库
```bash
git clone git@github.com:An0hana/fraser-diagram.git
```

### 3. 安装依赖
本项目主要依赖 `numpy` 和 `matplotlib`。
```bash
pip install -r requirements.txt
```


### 4. 运行
```bash
python main.py
```

## 指南

1.  **数据录入 (Data Entry)**：
    *   在 **X NODES** 输入等距节点
    *   在 **Y VALUES** 输入对应函数值
    *   在 **TARGET X** 输入待求插值点
2.  **开始制造 (Craft!)**：
    *   点击 **CRAFT** 按钮。
3.  **查看路径 (Interaction)**：
    *   在右侧 **LEDGER** 表格中，用鼠标点击任意一行（如 `Gauss F`）
    *   左侧地图将高亮显示该算法的计算路径。

## 项目结构

```text
fraser-diagram/
├── main.py          # 程序入口
├── calculator.py    # 插值算法计算
├── app.py           # 主窗口逻辑
├── theme.py         # 样式配置
├── plotter.py       # 绘图逻辑
├── logger.py        # 日志报告
├── README.md        # 项目说明
└── .gitignore       # Git忽略
```

## 算法

程序基于中心差分表，根据插值参数 $p = (x - x_0) / h$ 自动选择基准点，并演示以下公式：

| 方法 | 适用场景 | 路径特征 |
| :--- | :--- | :--- |
| **Newton Forward** | 插值点位于列表头部 | 向右下对角线延伸 |
| **Newton Backward**| 插值点位于列表尾部 | 向右上对角线延伸 |
| **Gauss Fwd/Bwd** | 插值点位于 $x_0$ 附近 | 之字形 (Zig-zag) |
| **Stirling** | $p \approx 0$ (靠近节点) | 高斯前向与后向的均值 |
| **Bessel** | $p \approx 0.5$ (靠近区间中点) | 涉及两个节点的加权 |


## 开源

本项目基于 MIT License 开源.

---