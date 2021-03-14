import pandas as pd
import numpy as np
import statsmodels.tsa.api as smt
import statsmodels.tsa.stattools as ts
import statsmodels.api as sm
import scipy.stats as scs
import matplotlib.pyplot as plt


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
        ts_ax.set_title(title+'时序图')
        smt.graphics.plot_acf(data, lags=lags, ax=acf_ax, alpha=0.5)
        acf_ax.set_title('自相关系数')
        smt.graphics.plot_pacf(data, lags=lags, ax=pacf_ax, alpha=0.5)
        pacf_ax.set_title('偏自相关系数')
        sm.qqplot(data, line='s', ax=qq_ax)
        qq_ax.set_title('QQ 图')
        scs.probplot(data, sparams=(data.mean(), data.std()), plot=pp_ax)
        pp_ax.set_title('PP 图')
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号“-”显示为方块的问题
        plt.tight_layout()
        plt.show()
    return


df = pd.read_csv('BTC.csv', header=0)
df['ret'] = np.log(df.Price/df.Price.shift(1))
max_lag = 30
Y = df.ret.dropna()

adf_check = ts.adfuller(Y, max_lag, regression='c', autolag='AIC', store=False, regresults=False)
print('平稳性检验结果：'+ str(adf_check))
ts_plot(Y,lags=max_lag,title='Bitcoin')