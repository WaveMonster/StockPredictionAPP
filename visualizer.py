import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk

# --- 问题修复代码块 [开始] ---

# 1. 解决中文显示问题：设置Matplotlib使用支持中文的字体
#    程序会依次尝试使用 'SimHei' (Windows常用), 'PingFang SC' (macOS常用)。
#    如果都没有，你需要自行安装一个中文字体, 例如 'Source Han Sans' (思源黑体)。
try:
    plt.rcParams['font.sans-serif'] = ['SimHei']
except:
    try:
        plt.rcParams['font.sans-serif'] = ['PingFang SC']
    except:
        print("警告：未找到 'SimHei' 或 'PingFang SC' 字体。中文可能无法正确显示。")
        print("请考虑安装支持中文的字体，如 'Source Han Sans'。")
        plt.rcParams['font.sans-serif'] = ['sans-serif']

# 2. 解决负号显示问题：在使用中文字体后，负号有时也会显示为方框。
plt.rcParams['axes.unicode_minus'] = False


# --- 问题修复代码块 [结束] ---


class StockVisualizer:
    def __init__(self, master=None):
        """初始化Visualizer，创建图布和坐标轴"""
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        # 如果在Tkinter主窗口中，则嵌入图表
        if master:
            self.canvas = FigureCanvasTkAgg(self.fig, master=master)
            self.canvas_widget = self.canvas.get_tk_widget()
            self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            toolbar = NavigationToolbar2Tk(self.canvas, master)
            toolbar.update()
            self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def plot_price_history(self, df_dict, title="股票价格历史", indicator_col=None):
        """绘制股价历史和可选指标"""
        self.ax.clear()
        for ticker, df in df_dict.items():
            if not df.empty:
                self.ax.plot(df.index, df['Close'], label=f'{ticker} 收盘价')
                if indicator_col and indicator_col in df.columns:
                    self.ax.plot(df.index, df[indicator_col], label=f'{ticker} {indicator_col}', linestyle='--')
        self._format_plot(title, "日期", "价格")

    def plot_multi_stock_comparison(self, df_dict, metric="Close", title="股票比较"):
        """比较多只股票的同一指标"""
        self.ax.clear()
        for ticker, df in df_dict.items():
            if not df.empty and metric in df.columns:
                self.ax.plot(df.index, df[metric], label=f'{ticker} {metric}')
        self._format_plot(title, "日期", metric)

    def _format_plot(self, title, xlabel, ylabel):
        """
        统一格式化图表。
        这是字体大小调整的核心位置。
        """
        # --- 字体大小调整 [开始] ---

        # 将标题字体大小设置为20
        self.ax.set_title(title, fontsize=20, weight='bold')

        # 将X轴和Y轴标签字体大小设置为16
        self.ax.set_xlabel(xlabel, fontsize=16)
        self.ax.set_ylabel(ylabel, fontsize=16)

        # 将图例字体大小设置为14
        self.ax.legend(fontsize=14)

        # 将坐标轴刻度字体大小设置为12
        self.ax.tick_params(axis='both', which='major', labelsize=12)

        # --- 字体大小调整 [结束] ---

        # 保持网格线和日期格式化
        self.ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        self.fig.tight_layout()  # 自动调整布局防止标签重叠
        self.fig.autofmt_xdate()

        # 刷新画布
        if hasattr(self, 'canvas'):
            self.canvas.draw()
        else:
            plt.show()