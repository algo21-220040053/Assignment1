# Assignment1
The project is an assignment about time series prediction for Algo Trading.
## Brief introduction
This article uses the classic time series model Arima to model and forecast the Bitcoin yield from March 1, 2017 to February 28, 2021.
## Model introduction
ARMA model is the combination of AR (P) and MA (q) models
1. AR (P) model tries to explain the momentum and mean reversion effects often observed in trading market.
2. The MA (q) model tries to explain the shock effect observed in white noise. These shock effects can be considered as unexpected events that affect the observation process, such as terrorist attacks.
The weakness of ARMA model is that it ignores the volatility aggregation effect in most financial time series.
<img width="427" alt="公式" src="https://user-images.githubusercontent.com/78734848/111869735-b4caa080-89bb-11eb-9827-ac542d2ea638.png">
ARIMA models is an extension of ARMA model. In reality, many time series are not stationary, but they can be stabilized by difference, that is, nonstationary machine can be transformed into stationary white noise by first-order difference. Because the ARMA model has the assumption that the time series are stationary, if the time series have a significant upward or downward trend, the prediction effect of the model is greatly discounted. For the data set with obvious downward or upward trend, it can be transformed into stationary series by difference method, and then fitted by ARMA model.
## Implementation process
First of all, the historical transaction data of BTC is used to calculate the rate of return. And output its sequence diagram, autocorrelation coefficient diagram, PP diagram, QQ diagram.
(img width="560" alt="BTC收益率图" src="https://user-images.githubusercontent.com/78734848/111869885-6538a480-89bc-11eb-89d6-ff233b5c4671.png")
Using ARIMA model, the optimal model is (3,0,3).
<img width="560" alt="arima实验结果" src="https://user-images.githubusercontent.com/78734848/111869878-5b16a600-89bc-11eb-8448-ffd4ad268465.png">
Output model residual diagram.
![BTC残差图](https://user-images.githubusercontent.com/78734848/111869906-7c779200-89bc-11eb-8423-dde8ec4dab3a.png)
The best model is a differential of 0 because we use yield data, as opposed to using the first time log difference to calculate the stock yield.The results of model residual diagram are basically the same as the original data above.Obviously, the ARIMA model is unable to explain the conditional volatility in the time series.
We use in-sample and out-of-sample predictions and output the following results:
![样本内预测](https://user-images.githubusercontent.com/78734848/111869954-cc565900-89bc-11eb-8957-7f952f2f1c5a.png)
![20天预测](https://user-images.githubusercontent.com/78734848/111869961-d2e4d080-89bc-11eb-9f98-d4bf0af42c22.png)

