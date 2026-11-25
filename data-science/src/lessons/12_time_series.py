from lib import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SEASONAL = [10, 20, 30, 15, 12, 22, 32, 17, 14, 24, 34, 19]

LESSON("Basics", "What makes time series different", """
<p>In most data the row order doesn't matter. In a <b>time series</b> — daily sales, hourly server load, monthly sign-ups — order is everything, and today's value depends on yesterday's. That changes three rules:</p>
<ul>
<li>The index is a date: parse it (<code>pd.to_datetime</code>), sort by it, and make the frequency explicit.</li>
<li>Missing dates are information: a day with no sales row usually means 0 sales, not "unknown".</li>
<li><b>Never shuffle.</b> Train on the past, test on the future, or your model peeks at answers.</li>
</ul>
<pre><code class="py">s = pd.Series(values, index=pd.to_datetime(days))
s.resample("W").sum()          # daily → weekly ("MS" monthly, "h" hourly)
s.asfreq("D", fill_value=0)    # put back the missing days</code></pre>
""", practice=["Daily to Weekly Totals", "Fill Missing Dates", "Average by Day of the Week"])

LESSON("Basics", "Lags, changes and smoothing", """
<pre><code class="py">s.shift(1)            # yesterday's value on today's row
s.diff()              # change since yesterday
s.pct_change(12)      # % change vs 12 periods ago (year over year for monthly data)
s.rolling(7).mean()   # 7-day moving average: hides day-to-day noise
s.ewm(alpha=0.3, adjust=False).mean()   # recent days count more</code></pre>
<p>A rolling average weights the last k values equally and drops older ones completely. An <b>exponential</b> moving average gives every past value some weight, shrinking by (1 − α) each step: a big α reacts fast, a small α is smooth. Comparing with the same period last year (YoY) removes seasonality from growth numbers.</p>
""", practice=["Lags and Differences", "Rolling Average", "Exponential Moving Average", "Year-over-Year Change", "Returns and Compound Growth"])


@LD
def smoothing_picture():
    s = pd.Series([12, 15, 14, 20, 13, 16, 15, 22, 14, 18, 17, 25], dtype=float)
    fig, ax = plt.subplots(figsize=(5, 2.6))
    ax.plot(s, marker="o", color="#94a3b8", label="sales")
    ax.plot(s.rolling(3).mean(), color="#0f766e", label="3-period average")
    ax.plot(s.ewm(alpha=0.3, adjust=False).mean(), color="#b45309", label="EMA α=0.3")
    ax.legend(fontsize=7)


LESSON("Core", "Trend, seasonality and autocorrelation", """
<p>Most series are a mix of three parts: <b>trend</b> (the long-run direction), <b>seasonality</b> (a pattern that repeats every m periods: weekdays, months, festivals) and <b>noise</b>. Classical decomposition estimates the trend with a centred moving average of length m, then averages what's left at each position in the cycle to get the seasonal indices.</p>
<p><b>Autocorrelation</b> at lag k is the correlation between the series and itself k steps earlier. A peak at lag 7 in daily data means a weekly pattern; at lag 12 in monthly data, a yearly one. It's the quickest way to find the season length.</p>
""", practice=["Seasonal Indices", "Autocorrelation at a Lag", "Find the Season Length"])


@LD
def seasonal_picture():
    s = pd.Series(SEASONAL, dtype=float)
    trend = s.rolling(4).mean().rolling(2).mean().shift(-2)
    fig, ax = plt.subplots(figsize=(5, 2.6))
    ax.plot(s, marker="o", color="#0f766e", label="data")
    ax.plot(trend, color="#b45309", label="trend (centred average)")
    ax.legend(fontsize=7)
    ax.set_title("A season of 4 on top of a rising trend")


LESSON("Core", "Forecasting: start with baselines", """
<p>Before any model, compute three <b>baselines</b>:</p>
<ul>
<li><b>Naive</b>: tomorrow = today. Hard to beat for stock prices and other random walks.</li>
<li><b>Mean</b>: the historical average. Good for stable, patternless series.</li>
<li><b>Seasonal naive</b>: next Monday = last Monday. Strong whenever there's seasonality.</li>
</ul>
<p>A fancy model is only worth it if it beats the best baseline on held-out data. Measure with <b>MAE</b> (average miss, in the data's units), <b>RMSE</b> (punishes big misses) or <b>MAPE</b> (percent, but breaks near zero).</p>
""", practice=["Baseline Forecasts", "Forecast Error Metrics", "Which Baseline Wins?"])

LESSON("Advanced", "Models: smoothing, trend lines and autoregression", """
<ul>
<li><b>Simple exponential smoothing</b> forecasts the latest smoothed level; choose α by the smallest one-step-ahead error. <b>Holt</b> adds a trend term and <b>Holt–Winters</b> a seasonal one (statsmodels' <code>ExponentialSmoothing</code>).</li>
<li><b>Linear trend</b>: regress the value on time. Fine for short horizons; dangerous to extrapolate far.</li>
<li><b>Autoregression AR(p)</b>: regress today on the last p values. ARIMA adds differencing (to remove trend) and moving-average error terms; SARIMA adds seasonality.</li>
<li><b>Machine learning</b>: turn the series into a table of lag features, rolling statistics and calendar features (weekday, month, holiday), then use gradient boosting. This is how most large-scale demand forecasting is done today; Prophet and deep models (N-BEATS, temporal transformers) are other options.</li>
</ul>
""", practice=["Straight-Line Trend Forecast", "Tune the Smoothing Factor", "Autoregressive Forecast AR(1)", "Turn a Series into a Supervised Dataset"])

LESSON("Advanced", "Validating forecasts honestly, and spotting anomalies", """
<p><b>Walk-forward validation</b>: train on data up to a cut-off, forecast the next block, move the cut-off forward, repeat. Average the errors over the folds. It mimics how the model will really be used. Features must only use information available at forecast time — a 7-day rolling mean that includes today leaks today's answer.</p>
<p><b>Anomaly detection</b> flags values far from what the recent past predicts: compare each point with the mean and standard deviation of the window <i>before</i> it. Note one big spike inflates the next windows' standard deviation and can hide a second anomaly; robust versions use the median and the median absolute deviation instead.</p>
""", practice=["Walk-Forward Validation Splits", "Flag Anomalies"])
