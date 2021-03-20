import pandas as pd
import numpy as np
import statsmodels.tsa.api as smt
import statsmodels.api as sm
import scipy.stats as scs
import matplotlib.pyplot as plt


class ArimaMethod:
    def __init__(self, data, df):
        self.data = data
        self.df = df
        self.best_aic = None
        self.best_order = None
        self.best_mdl = None

    @staticmethod
    def ts_plot(data, lags=None, title=''):
        if not isinstance(data, pd.Series):
            data = pd.Series(data)
        with plt.style.context('ggplot'):
            fig = plt.figure(figsize=(10, 8))
            layout = (3, 2)
            ts_ax = plt.subplot2grid(layout, (0, 0), colspan=2)
            acf_ax = plt.subplot2grid(layout, (1, 0))
            pacf_ax = plt.subplot2grid(layout, (1, 1))
            qq_ax = plt.subplot2grid(layout, (2, 0))
            pp_ax = plt.subplot2grid(layout, (2, 1))

            data.plot(ax=ts_ax)
            ts_ax.set_title(title + '时序图')
            smt.graphics.plot_acf(data, lags=lags, ax=acf_ax, alpha=0.5)
            acf_ax.set_title('自相关系数')
            smt.graphics.plot_pacf(data, lags=lags, ax=pacf_ax, alpha=0.5)
            pacf_ax.set_title('偏自相关系数')
            sm.qqplot(data, line='s', ax=qq_ax)
            qq_ax.set_title('QQ 图')
            scs.probplot(data, sparams=(data.mean(), data.std()), plot=pp_ax)
            pp_ax.set_title('PP 图')
            plt.rcParams['font.sans-serif'] = ['SimHei']
            plt.rcParams['axes.unicode_minus'] = False
            plt.tight_layout()
            plt.show()
        return

    def get_best_model(self, pq, d):        # 使用AIC法则对模型定阶
        best_aic = np.inf
        best_order = None
        best_mdl = None
        pq_rng = range(pq)
        d_rng = range(d)
        for i in pq_rng:
            for d in d_rng:
                for j in pq_rng:
                    try:
                        tmp_mdl = smt.ARIMA(self.data, order=(i, d, j)).fit(method='mle', trend='nc')
                        tmp_aic = tmp_mdl.aic
                        if tmp_aic < best_aic:
                            best_aic = tmp_aic
                            best_order = (i, d, j)
                            best_mdl = tmp_mdl
                    except:
                        continue
        print('aic: {:6.5f} | order: {}'.format(best_aic, best_order))
        self.best_aic = best_aic
        self.best_order = best_order
        self.best_mdl = best_mdl

    def show_resid(self, lag):   # 对拟合残差进行可视化
        resid = pd.Series(self.best_mdl.resid, index=self.data.index)
        self.ts_plot(resid, lags=lag, title='BTC价格ARIMA残差')

    def prediction(self):       # 样本内预测,并进行可视化
        plt.style.use('ggplot')
        fig = plt.figure(figsize=(12, 7))
        ax = plt.gca()
        ts = self.data[-500:].copy()
        ts.plot(ax=ax, label='HS300收益率')
        # 样本内预测
        pred = self.best_mdl.predict(start=961, end=1460, dynamic=False)
        pf = pd.Series(pred, index=ts.index)
        pf.plot(ax=ax, style='r-', label='样本内预测')
        plt.title('样本内预测')
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.legend()
        plt.show()

    def forecast(self, n_steps):       # 样本外预测,并进行可视化
        f, err95, ci95 = self.best_mdl.forecast(steps=n_steps)
        b, err99, ci99 = self.best_mdl.forecast(steps=n_steps, alpha=0.01)
        date = self.df.values[-1:, 0]
        idx = pd.date_range(start=date[0], periods=n_steps + 1, closed='right')
        fc_95 = pd.DataFrame(np.column_stack([f, ci95]),
                             index=idx, columns=['forecast', 'lower_ci_95', 'upper_ci_95'])
        fc_99 = pd.DataFrame(np.column_stack([ci99]),
                             index=idx, columns=['lower_ci_99', 'upper_ci_99'])
        fc_all = fc_95.combine_first(fc_99)

        fc_all.index = pd.to_datetime(fc_all.index)
        fc_all.plot()
        plt.fill_between(fc_all.index, fc_all.lower_ci_95, fc_all.upper_ci_95, color='gray', alpha=0.7)
        plt.fill_between(fc_all.index, fc_all.lower_ci_99, fc_all.upper_ci_99, color='gray', alpha=0.2)
        plt.title('{} 天BTC收益率预测\nARIMA{}'.format(n_steps, self.best_order))
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.legend(loc='best', fontsize=10)
        plt.show()


if __name__ == '__main__':
    df = pd.read_csv('BTC.csv', header=0)
    df['ret']=np.log(df.Price/df.Price.shift(1))
    Y = df.ret.dropna()
    ts = ArimaMethod(Y, df)
    max_lag = 30
    ts.ts_plot(ts.data,max_lag, 'Bitcoin')
    ts.get_best_model(2,2)
    # 对拟合残差进行可视化
    ts.show_resid(max_lag)
    # 对BTC历史收益率进行预测
    ts.prediction()
    # 对BTC收益率未来5天进行预测
    steps = 5
    ts.forecast(steps)
