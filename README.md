\# 股票分析与估值工具 (Stock Analysis \& Valuation Tool)



这是一个使用 Python 构建的桌面应用程序，旨在为用户提供一个简单、直观的工具来获取、可视化和评估上市公司的价值。



---



\## 核心功能 (Features)



\- \*\*实时数据获取\*\*: 从 Yahoo Finance 动态抓取股票的实时市场数据和历史财务报表。

\- \*\*多模型估值\*\*:

&nbsp; - \*\*折现现金流 (DCF) 模型\*\*: 基于未来的自由现金流预测，估算公司的内在价值。

&nbsp; - \*\*本杰明·格雷厄姆 (Benjamin Graham) 模型\*\*: 运用价值投资之父的经典公式，为成长股提供一个合理的内在价值估算。

&nbsp; - \*\*相对估值模型\*\*: 通过与竞争对手的市盈率(P/E)、市销率(P/S)、市净率(P/B)等关键指标对比，评估公司当前的市场定位。

\- \*\*数据可视化\*\*:

&nbsp; - 绘制股价历史走势图。

&nbsp; - 支持将目标公司与多个竞争对手的股价进行同图对比。

\- \*\*财务报表查阅\*\*: 在程序界面内直接展示公司的年度利润表、资产负债表和现金流量表。



\## 技术栈 (Technology Stack)



\- \*\*Python 3\*\*: 主要编程语言。

\- \*\*Tkinter\*\*: 用于构建图形用户界面 (GUI)。

\- \*\*yfinance\*\*: 用于从 Yahoo Finance 获取股票数据。

\- \*\*Pandas\*\*: 用于数据处理和分析。

\- \*\*Matplotlib\*\*: 用于数据可视化和图表绘制。



\## 如何开始 (Getting Started)



请按照以下步骤在您的本地计算机上设置并运行此项目。



\### 准备工作



\- 确保您的计算机上已安装 \[Python 3.9](https://www.python.org/downloads/) 或更高版本。

\- 确保已安装 `pip` (Python 包管理器)。



\### 安装步骤



1\.  \*\*克隆仓库\*\*

&nbsp;   ```bash

&nbsp;   git clone \[https://github.com/YourUsername/Stock-Valuation-Tool.git](https://github.com/YourUsername/Stock-Valuation-Tool.git)

&nbsp;   cd Stock-Valuation-Tool

&nbsp;   ```



2\.  \*\*创建 `requirements.txt` 文件\*\*

&nbsp;   在您的项目文件夹根目录下，创建一个名为 `requirements.txt` 的文件，并将以下内容复制进去：

&nbsp;   ```

&nbsp;   yfinance

&nbsp;   pandas

&nbsp;   matplotlib

&nbsp;   beautifulsoup4

&nbsp;   requests

&nbsp;   lxml

&nbsp;   scipy

&nbsp;   ```



3\.  \*\*安装依赖包\*\*

&nbsp;   在终端中运行以下命令来安装所有必需的库：

&nbsp;   ```bash

&nbsp;   pip install -r requirements.txt

&nbsp;   ```



\### 运行程序



安装完所有依赖后，运行主程序文件：

```bash

python main\_app.py

