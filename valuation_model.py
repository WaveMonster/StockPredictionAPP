import numpy as np


class StockValuationModel:
    def __init__(self, risk_free_rate=0.04, market_return=0.09, corporate_tax_rate=0.21):
        self.risk_free_rate = risk_free_rate
        self.market_return = market_return
        self.corporate_tax_rate = corporate_tax_rate

    def calculate_cost_of_equity(self, beta):
        """使用CAPM模型计算股权成本 (Re)"""
        return self.risk_free_rate + beta * (self.market_return - self.risk_free_rate)

    def calculate_wacc(self, market_cap, total_debt, cost_of_equity, cost_of_debt):
        """计算加权平均资本成本 (WACC)"""
        V = market_cap + total_debt
        if V == 0: return np.nan
        equity_weight = market_cap / V
        debt_weight = total_debt / V
        wacc = (equity_weight * cost_of_equity) + (debt_weight * cost_of_debt * (1 - self.corporate_tax_rate))
        return wacc

    def dcf_valuation(self, current_fcf, growth_rates_high, terminal_growth_rate,
                      wacc, shares_outstanding, total_debt, cash_equivalents):
        """折现现金流 (DCF) 估值模型"""
        if wacc <= terminal_growth_rate:
            raise ValueError("WACC 必须大于永续增长率")

        projected_fcf_discounted = []
        fcf_t = current_fcf

        for i, growth_rate in enumerate(growth_rates_high):
            fcf_t *= (1 + growth_rate)
            projected_fcf_discounted.append(fcf_t / ((1 + wacc) ** (i + 1)))

        # 计算终值并折现
        last_fcf = fcf_t
        terminal_value = (last_fcf * (1 + terminal_growth_rate)) / (wacc - terminal_growth_rate)
        discounted_terminal_value = terminal_value / ((1 + wacc) ** len(growth_rates_high))

        enterprise_value = sum(projected_fcf_discounted) + discounted_terminal_value
        equity_value = enterprise_value - total_debt + cash_equivalents

        if shares_outstanding == 0: return np.nan
        per_share_value = equity_value / shares_outstanding
        return per_share_value

    def relative_valuation(self, target_eps, target_sales_per_share, target_book_value_per_share,
                           competitor_avg_pe=None, competitor_avg_ps=None, competitor_avg_pb=None):
        """相对估值模型"""
        valuations = {}
        if competitor_avg_pe and target_eps:
            valuations['市盈率(P/E)法'] = target_eps * competitor_avg_pe
        if competitor_avg_ps and target_sales_per_share:
            valuations['市销率(P/S)法'] = target_sales_per_share * competitor_avg_ps
        if competitor_avg_pb and target_book_value_per_share:
            valuations['市净率(P/B)法'] = target_book_value_per_share * competitor_avg_pb
        return valuations
# 在 valuation_model.py 的 StockValuationModel 类中添加此方法

    def benjamin_graham_valuation(self, eps, g, Y):
        """
        使用修订版格雷厄姆公式计算内在价值。
        V = (EPS * (8.5 + 2g) * 4.4) / Y
        :param eps: 最近12个月的每股收益
        :param g: 预期的年化增长率 (例如，输入15表示15%)
        :param Y: 当前高等级公司债券收益率 (例如，输入4.5表示4.5%)
        :return: 每股内在价值
        """
        if Y is None or Y == 0:
            return None
        # 为了防止对超高增长公司给出不切实际的估值，格雷厄姆建议对增长率g进行限制
        g = min(g, 20.0) # 将增长率的上限设为20%
        value = (eps * (8.5 + 2 * g) * 4.4) / Y
        return value