import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import numpy as np
import yfinance as yf  # 确保 yfinance 已导入

from data_fetcher import YahooFinanceDataFetcher
from data_processor import StockDataProcessor
from visualizer import StockVisualizer
from valuation_model import StockValuationModel


class StockAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("股票估值与可视化工具")
        self.root.geometry("1200x800")

        self.fetcher = YahooFinanceDataFetcher()
        self.processor = StockDataProcessor()
        self.valuation_model = StockValuationModel(risk_free_rate=0.04, market_return=0.09)

        self.fetched_data = {}
        self._create_widgets()

    def _create_widgets(self):
        # GUI布局代码与之前版本相同
        input_frame = ttk.LabelFrame(self.root, text="股票信息输入")
        input_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        ttk.Label(input_frame, text="主股票代码/名称:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.main_ticker_entry = ttk.Entry(input_frame, width=20)
        self.main_ticker_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        self.main_ticker_entry.insert(0, "NVDA")

        ttk.Label(input_frame, text="竞争对手代码 (逗号分隔):").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.competitors_entry = ttk.Entry(input_frame, width=40)
        self.competitors_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
        self.competitors_entry.insert(0, "AMD,INTC")

        self.run_button = ttk.Button(input_frame, text="获取数据并分析", command=self.analyze_stock)
        self.run_button.grid(row=0, column=2, rowspan=2, padx=10, pady=5, sticky="ns")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.plot_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.plot_frame, text="图表分析")
        self.visualizer = StockVisualizer(master=self.plot_frame)

        self.financials_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.financials_frame, text="财务报表")
        self.financials_text = scrolledtext.ScrolledText(self.financials_frame, wrap=tk.WORD, width=100, height=20)
        self.financials_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.valuation_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.valuation_frame, text="估值结果")
        self.valuation_output = scrolledtext.ScrolledText(self.valuation_frame, wrap=tk.WORD, width=100, height=20)
        self.valuation_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def analyze_stock(self):
        self.run_button.config(state="disabled", text="分析中...")
        self.root.update_idletasks()

        main_ticker = self.main_ticker_entry.get().strip().upper()
        if not main_ticker:
            messagebox.showerror("错误", "请输入主股票代码。")
            self.run_button.config(state="normal", text="获取数据并分析")
            return

        competitor_tickers = [t.strip() for t in self.competitors_entry.get().strip().upper().split(',') if t.strip()]
        all_tickers = [main_ticker] + competitor_tickers
        self.fetched_data = {}

        for ticker in all_tickers:
            print(f"正在获取 {ticker} 的数据...")
            data = self._fetch_and_process_single_stock(ticker)
            if not data['info']:
                messagebox.showwarning("警告", f"无法获取 {ticker} 的数据，请检查股票代码。")
                continue
            self.fetched_data[ticker] = data

        if main_ticker not in self.fetched_data:
            messagebox.showerror("错误", f"无法获取主股票 {main_ticker} 的数据。分析中止。")
            self.run_button.config(state="normal", text="获取数据并分析")
            return

        print("所有数据获取完毕，开始展示...")
        self._display_financials(main_ticker)
        self._calculate_and_display_valuation(main_ticker, competitor_tickers)
        self._plot_data(main_ticker, competitor_tickers)

        self.run_button.config(state="normal", text="获取数据并分析")

    def _fetch_and_process_single_stock(self, ticker):
        data = {
            'info': self.fetcher.get_company_info(ticker),
            'history': self.fetcher.get_stock_history(ticker, period="5y"),
            'financials': self.fetcher.get_financials(ticker)
        }
        if data['info']:
            data['processed_history'] = self.processor.calculate_technical_indicators(data['history'])
            data['annual_cash_flow'] = self.processor.get_yearly_financial_data(data['financials'], 'cash_flow')
            data['annual_balance'] = self.processor.get_yearly_financial_data(data['financials'], 'balance_sheet')
            data['annual_income'] = self.processor.get_yearly_financial_data(data['financials'], 'income_stmt')
            data['fcf'] = self.processor.calculate_free_cash_flow(data['annual_cash_flow'])
            data['total_debt'] = self.processor.get_total_debt(data['annual_balance'])
            data['cash_equivalents'] = self.processor.get_cash_and_equivalents(data['annual_balance'])
            data['total_equity'] = self.processor.get_total_stockholder_equity(data['annual_balance'])
            # (新增) 获取EPS历史数据用于计算增长率
            data['eps_history'] = self.processor.get_eps_from_financials(data['annual_income'])
        return data

    def _plot_data(self, main_ticker, competitor_tickers):
        plot_dfs = {}
        if main_ticker in self.fetched_data:
            plot_dfs[main_ticker] = self.fetched_data[main_ticker]['processed_history']
        for ticker in competitor_tickers:
            if ticker in self.fetched_data:
                plot_dfs[ticker] = self.fetched_data[ticker]['processed_history']
        self.visualizer.plot_multi_stock_comparison(plot_dfs, title="收盘价对比 (5年)")

    def _display_financials(self, main_ticker):
        self.financials_text.delete(1.0, tk.END)
        data = self.fetched_data[main_ticker]
        self.financials_text.insert(tk.END, f"--- {main_ticker} 关键财务数据 ---\n\n")
        for key in ['income_stmt', 'balance_sheet', 'cash_flow']:
            self.financials_text.insert(tk.END, f"--- {key.replace('_', ' ').title()} ---\n")
            df = data['financials'].get(key)
            if df is not None and not df.empty:
                self.financials_text.insert(tk.END, df.to_string() + "\n\n")
            else:
                self.financials_text.insert(tk.END, "数据不可用\n\n")

    def _calculate_and_display_valuation(self, main_ticker, competitor_tickers):
        self.valuation_output.delete(1.0, tk.END)
        main_data = self.fetched_data[main_ticker]
        output = f"--- {main_ticker} 估值分析 ---\n\n"

        # (新增) 获取格雷厄姆公式所需的Y值
        current_yield_Y = self.fetcher.get_current_yield("^TNX")

        # --- DCF 估值 ---
        # (代码无变化, 保持原样)
        output += "### 1. 折现现金流 (DCF) 估值 ###\n"
        # ... (此处省略未改变的DCF代码) ...
        try:
            beta = main_data['info'].get('beta')
            market_cap = main_data['info'].get('marketCap')
            shares_outstanding = main_data['info'].get('sharesOutstanding')
            current_fcf = main_data['fcf'].iloc[-1] if not main_data['fcf'].empty else None
            total_debt = main_data['total_debt'].iloc[-1] if not main_data['total_debt'].empty else None
            cash_equivalents = main_data['cash_equivalents'].iloc[-1] if not main_data[
                'cash_equivalents'].empty else None
            required_data_map = {'Beta值': beta, '市值': market_cap, '流通股数': shares_outstanding,
                                 '最新自由现金流': current_fcf, '总负债': total_debt, '现金及等价物': cash_equivalents}
            missing_items = [name for name, value in required_data_map.items() if value is None]
            if not missing_items:
                if len(main_data['fcf']) > 1:
                    hist_growth = main_data['fcf'].pct_change().mean()
                    growth_rates_high = [max(min(hist_growth * (1 - 0.1 * i), 0.3), 0.05) for i in range(5)]
                else:
                    growth_rates_high = [0.15, 0.12, 0.10, 0.08, 0.05]
                terminal_growth_rate = 0.025;
                cost_of_debt = 0.055
                cost_of_equity = self.valuation_model.calculate_cost_of_equity(beta);
                wacc = self.valuation_model.calculate_wacc(market_cap, total_debt, cost_of_equity, cost_of_debt)
                output += f"  - WACC 计算参数: Beta={beta:.2f}, 股权成本={cost_of_equity:.2%}, WACC={wacc:.2%}\n"
                output += f"  - FCF 增长假设 (5年): {[f'{g:.2%}' for g in growth_rates_high]}\n"
                dcf_value = self.valuation_model.dcf_valuation(current_fcf, growth_rates_high, terminal_growth_rate,
                                                               wacc, shares_outstanding, total_debt, cash_equivalents)
                output += f"  >>> DCF 每股内在价值: ${dcf_value:.2f}\n"
            else:
                output += f"  - 关键数据不足，无法进行DCF估值。\n";
                output += f"  - 缺失的项目: {', '.join(missing_items)}\n"
        except Exception as e:
            output += f"  - DCF 估值计算出错: {e}\n"

        # --- (新增) 本杰明·格雷厄姆估值 ---
        output += "\n### 2. 本杰明·格雷厄姆估值 ###\n"
        try:
            eps = main_data['info'].get('trailingEps')
            eps_history = main_data.get('eps_history')
            g = None
            if eps_history is not None and len(eps_history) > 2:
                # 计算3年复合年均增长率(CAGR)作为g的代理
                # 过滤负值或零值以避免计算错误
                eps_history_positive = eps_history[eps_history > 0]
                if len(eps_history_positive) > 2:
                    end_value = eps_history_positive.iloc[-1]
                    start_value = eps_history_positive.iloc[-3]
                    cagr = ((end_value / start_value) ** (1 / 2)) - 1
                    g = cagr * 100  # 转换为百分比

            if all([eps, g is not None, current_yield_Y]):
                output += f"  - 计算参数: EPS=${eps:.2f}, 历史EPS增长率g={g:.2f}%, 债券收益率Y={current_yield_Y:.2f}%\n"
                graham_value = self.valuation_model.benjamin_graham_valuation(eps, g, current_yield_Y)
                output += f"  >>> 格雷厄姆内在价值: ${graham_value:.2f}\n"
            else:
                output += "  - 关键数据不足 (如 EPS, EPS历史增长率, 或债券收益率)，无法进行估值。\n"
        except Exception as e:
            output += f"  - 格雷厄姆估值计算出错: {e}\n"

        # --- 相对估值 ---
        output += "\n### 3. 相对估值 ###\n"
        # (代码无变化, 保持原样)
        try:
            pe_list, ps_list, pb_list = [], [], []
            for ticker in competitor_tickers:
                if ticker in self.fetched_data:
                    info = self.fetched_data[ticker]['info']
                    if info.get('trailingPE'): pe_list.append(info['trailingPE'])
                    if info.get('priceToSalesTrailing12Months'): ps_list.append(info['priceToSalesTrailing12Months'])
                    if info.get('priceToBook'): pb_list.append(info['priceToBook'])
            avg_pe = np.mean(pe_list) if pe_list else None;
            avg_ps = np.mean(ps_list) if ps_list else None;
            avg_pb = np.mean(pb_list) if pb_list else None
            pe_str = f"{avg_pe:.2f}" if avg_pe is not None else "N/A";
            ps_str = f"{avg_ps:.2f}" if avg_ps is not None else "N/A";
            pb_str = f"{avg_pb:.2f}" if avg_pb is not None else "N/A"
            output += f"  - 竞争对手平均倍数: P/E={pe_str}, P/S={ps_str}, P/B={pb_str}\n"
            target_eps = main_data['info'].get('trailingEps')
            total_revenue = main_data['annual_income'].loc['Total Revenue'].iloc[-1] if 'Total Revenue' in main_data[
                'annual_income'].index else None
            total_equity = main_data['total_equity'].iloc[-1] if not main_data['total_equity'].empty else None
            shares_outstanding = main_data['info'].get('sharesOutstanding')
            target_sps = total_revenue / shares_outstanding if total_revenue and shares_outstanding else None;
            target_bps = total_equity / shares_outstanding if total_equity and shares_outstanding else None
            relative_values = self.valuation_model.relative_valuation(target_eps, target_sps, target_bps, avg_pe,
                                                                      avg_ps, avg_pb)
            if not relative_values:
                output += "  - 关键数据不足 (如 EPS, 股东权益等)，无法进行相对估值。\n"
            else:
                for method, value in relative_values.items(): output += f"  >>> 基于 {method} 的估值: ${value:.2f}\n"
        except Exception as e:
            output += f"  - 相对估值计算出错: {e}\n"

        output += f"\n### 当前市场价格 ###\n  - {main_ticker} 当前股价: ${main_data['history']['Close'].iloc[-1]:.2f}\n"
        self.valuation_output.insert(tk.END, output)


if __name__ == "__main__":
    root = tk.Tk()
    app = StockAnalysisApp(root)
    root.mainloop()