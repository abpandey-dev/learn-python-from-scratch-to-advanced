from lib import *

THEORY("Components", """
<table>
<tr><th>Part</th><th>Meaning</th><th>Example</th></tr>
<tr><td>Trend</td><td>long-run rise or fall</td><td>growing user base</td></tr>
<tr><td>Seasonality</td><td>fixed-length repeating pattern</td><td>weekend peaks, Diwali sales</td></tr>
<tr><td>Cycle</td><td>rises and falls without a fixed length</td><td>economic cycles</td></tr>
<tr><td>Noise</td><td>what's left</td><td>random day-to-day variation</td></tr>
</table>
<p><b>Additive</b>: y = trend + season + noise (seasonal swings stay the same size). <b>Multiplicative</b>: y = trend × season × noise (swings grow with the level); taking logs turns it additive.</p>
""")

THEORY("Stationarity", """
<p>A series is <b>stationary</b> if its mean, variance and autocorrelation don't change over time. Many classical models (ARIMA) assume it. Make a series more stationary by <b>differencing</b> (removes trend), <b>seasonal differencing</b> (x<sub>t</sub> − x<sub>t−m</sub>) and <b>log transforms</b> (stabilises growing variance). The Augmented Dickey–Fuller test checks it formally.</p>
""")

THEORY("Error metrics", """
<table>
<tr><th>Metric</th><th>Formula</th><th>Note</th></tr>
<tr><td>MAE</td><td>mean |y − ŷ|</td><td>same units as data, robust</td></tr>
<tr><td>RMSE</td><td>√mean (y − ŷ)²</td><td>punishes large errors</td></tr>
<tr><td>MAPE</td><td>mean |y − ŷ| / |y|</td><td>undefined at y = 0, favours under-forecasts</td></tr>
<tr><td>MASE</td><td>MAE / MAE of the naive forecast</td><td>&lt; 1 beats naive; comparable across series</td></tr>
</table>
""")

FAQ("Why can't you use ordinary k-fold cross-validation on time series?", "<p>Random folds put future rows in the training set, so the model learns from the future and the score is too optimistic. Use time-ordered splits (walk-forward / TimeSeriesSplit).</p>")
FAQ("What is autocorrelation?", "<p>The correlation of a series with a lagged copy of itself. Peaks at regular lags reveal seasonality; slowly decaying autocorrelation suggests a trend.</p>")
FAQ("How would you forecast daily sales for 1,000 stores?", "<p>Start with seasonal-naive baselines, then one global gradient-boosting model with lag, rolling and calendar features plus store attributes, validated walk-forward, and compared with the baseline per store.</p>")
FAQ("What does differencing do?", "<p>It replaces values with their changes, removing a trend so the series becomes closer to stationary.</p>")
FAQ("Moving average vs exponential smoothing?", "<p>A moving average weights the last k points equally; exponential smoothing weights all past points with weights that decay geometrically, so it reacts faster and needs only the last level to update.</p>")
FAQ("What is data leakage in forecasting?", "<p>Using information that wouldn't exist at prediction time, such as a rolling mean that includes the target day, or scaling with statistics from the whole series.</p>")
