# Assignment1
The project is an assignment about time series prediction for Algo Trading.
## Brief introduction
This article uses the classic time series model Arima to model and forecast the Bitcoin yield from March 1, 2017 to February 28, 2021. And try to improve the model by GARCH.
## Model introduction
ARMA model is the combination of AR (P) and MA (q) models
1. AR (P) model tries to explain the momentum and mean reversion effects often observed in trading market.
2. The MA (q) model tries to explain the shock effect observed in white noise. These shock effects can be considered as unexpected events that affect the observation process, such as terrorist attacks.
The weakness of ARMA model is that it ignores the volatility aggregation effect in most financial time series.  

<div align=center><img width="427" alt="公式" src="https://user-images.githubusercontent.com/78734848/111869735-b4caa080-89bb-11eb-9827-ac542d2ea638.png"><div align=left>
  
ARIMA models is an extension of ARMA model. In reality, many time series are not stationary, but they can be stabilized by difference, that is, nonstationary machine can be transformed into stationary white noise by first-order difference. Because the ARMA model has the assumption that the time series are stationary, if the time series have a significant upward or downward trend, the prediction effect of the model is greatly discounted. For the data set with obvious downward or upward trend, it can be transformed into stationary series by difference method, and then fitted by ARMA model.
The ARCH model was developed by Engle in 1982 when he analyzed the UK inflation rate. It was mainly used to characterize the statistical characteristics of fluctuations.The generalized conditional heteroscedasticity model is an extension of the ARCH model, that is, the conditional variance of the GARCH model is not only a linear function of the square of the lag residuals, but also a linear function of the lag conditional variance.
## Implementation process
First of all, the historical transaction data of BTC is used to calculate the rate of return. And output its sequence diagram, autocorrelation coefficient diagram, PP diagram, QQ diagram.

<div align=center><img width="640" alt="BTC收益率图" src="https://user-images.githubusercontent.com/78734848/111870129-d3319b80-89bd-11eb-9cbb-10199f4b3f53.png"><div align=left>
  
Using ARIMA model, the optimal model is (3,0,3).

<div align=center><img width="560" alt="arima实验结果" src="https://user-images.githubusercontent.com/78734848/111869878-5b16a600-89bc-11eb-8448-ffd4ad268465.png"><div align=left>
  
Output model residual diagram.

<div align=center><img width="640" alt="BTC残差图" src="https://user-images.githubusercontent.com/78734848/111869906-7c779200-89bc-11eb-8423-dde8ec4dab3a.png"><div align=left>
  
The best model is a differential of 0 because we use yield data, as opposed to using the first time log difference to calculate the stock yield.The results of model residual diagram are basically the same as the original data above.Obviously, the ARIMA model is unable to explain the conditional volatility in the time series.
We use in-sample and out-of-sample predictions and output the following results:
<div align=center><img width="640" alt="样本内预测" src="https://user-images.githubusercontent.com/78734848/111869954-cc565900-89bc-11eb-8957-7f952f2f1c5a.png">
<img width="420" alt="20天预测" src="https://user-images.githubusercontent.com/78734848/111869961-d2e4d080-89bc-11eb-9f98-d4bf0af42c22.png"><div align=left>

## Improvement
The conditional variance of yield varies over time, that is, the characteristic of conditional heteroscedasticity.The fluctuations of the yield series are persistent, that is, there is a phenomenon of Volatility Clustering, which has a large fluctuation.QQ plot shows that the return rate does not follow normal distribution, there are more extreme values, and there is a phenomenon of thick tail.
So we try to use GARCH model to solve this problem.
The model detail is the following:
<div align=center><img width="589" alt="GARCH实验结果" src="https://user-images.githubusercontent.com/78734848/111871174-c7e16e80-89c3-11eb-9ca3-8f7a5182d55d.png"><div align=left>
Output model residual diagram.
<div align=center><img width="640" alt="BTC残差图" src="https://user-images.githubusercontent.com/78734848/111871244-da5ba800-89c3-11eb-9628-a9d38d7deee0.png"><div align=left>
  There is not a great different between the residual diagram of ARIMA model and GARCH model. GARCH model does not fit the data quite well.


