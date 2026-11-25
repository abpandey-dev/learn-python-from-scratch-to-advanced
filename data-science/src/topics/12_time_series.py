from lib import *
import math
from datetime import date, timedelta
import numpy as np
import pandas as pd


TOPIC(
    id="time-series", title="Time Series & Forecasting", glyph="📈",
    blurb="Work with data ordered in time: resampling and missing dates, lags, rolling and exponential averages, trend and seasonality, autocorrelation, baseline and smoothing forecasts, autoregression, honest time-based validation, forecast errors and anomaly flags.",
    theory="""
<h3>Cheat sheet</h3>
<pre><code class="py">s = df.set_index(pd.to_datetime(df.day))["sales"]
s.resample("W").sum(); s.asfreq("D", fill_value=0)     # change frequency, fill gaps
s.shift(1); s.diff(); s.pct_change()                  # lags and changes
s.rolling(7).mean(); s.ewm(alpha=0.3, adjust=False).mean()
s.autocorr(lag=7)                                     # repeating pattern every 7?
s.index.day_name(); s.groupby(s.index.day_of_week).mean()
train, test = s[:-14], s[-14:]                        # never shuffle time
np.polyfit(t, y, 1)                                   # straight-line trend</code></pre>
""")

SALES = [12, 15, 14, 20, 13, 16, 15, 22, 14, 18, 17, 25]
SEASONAL = [10, 20, 30, 15, 12, 22, 32, 17, 14, 24, 34, 19]


Q(None, "Daily to Weekly Totals", "Easy", "resample",
  "<code>days</code> are ISO dates with <code>values</code>. Return weekly totals keyed by the week's last day (Sunday), like pandas <code>resample('W')</code>.",
  [((["2026-03-02", "2026-03-04", "2026-03-08", "2026-03-09", "2026-03-15"], [5, 3, 2, 7, 1]), {'2026-03-08': 10, '2026-03-15': 8})],
  ("For each date, jump forward to its Sunday and add into a dict.", "O(n)", "O(weeks)"),
  ("A DatetimeIndex and <code>resample('W').sum()</code>.", "O(n)", "O(weeks)"),
  viz=(["2026-03-02", "2026-03-04", "2026-03-08", "2026-03-09"], [5, 3, 2, 7]))


@B
def weekly(days, values):
    out = {}
    for d, v in zip(days, values):
        day = date.fromisoformat(d)
        sunday = day + timedelta(days=6 - day.weekday())
        out[str(sunday)] = out.get(str(sunday), 0) + v
    return dict(sorted(out.items()))


@O
def weekly(days, values):
    s = pd.Series(values, index=pd.to_datetime(days)).resample("W").sum()
    return {str(k.date()): int(v) for k, v in s.items()}


Q(None, "Fill Missing Dates", "Easy", "asfreq",
  "Sales data skips days with no sales. Return the full daily list of values from the first to the last date, with 0 on missing days.",
  [((["2026-03-01", "2026-03-02", "2026-03-05"], [4, 6, 1]), [4, 6, 0, 0, 1])],
  ("Walk day by day with <code>timedelta</code>, using a dict lookup.", "O(days)", "O(n)"),
  ("<code>asfreq('D', fill_value=0)</code>.", "O(days)", "O(days)"),
  viz=(["2026-03-01", "2026-03-02", "2026-03-05"], [4, 6, 1]))


@B
def fill_days(days, values):
    known = dict(zip(days, values))
    d, end = date.fromisoformat(days[0]), date.fromisoformat(days[-1])
    out = []
    while d <= end:
        out.append(known.get(str(d), 0))
        d += timedelta(days=1)
    return out


@O
def fill_days(days, values):
    return pd.Series(values, index=pd.to_datetime(days)).asfreq("D", fill_value=0).tolist()


Q(None, "Lags and Differences", "Easy", "shift · diff",
  "Return <code>(lag-1 values, first differences)</code>, with None where there's no earlier value.",
  [((SALES[:5],), ([None, 12.0, 15.0, 14.0, 20.0], [None, 3.0, -1.0, 6.0, -7.0]))],
  ("Index arithmetic in a loop.", "O(n)", "O(n)"),
  ("<code>s.shift(1)</code> and <code>s.diff()</code>.", "O(n)", "O(n)"),
  viz=(SALES[:5],))


@B
def lags(values):
    lag = [None] + values[:-1]
    diff = [None] + [values[i] - values[i - 1] for i in range(1, len(values))]
    return (lag, diff)


@O
def lags(values):
    s = pd.Series(values, dtype=float)
    return (s.shift(1).tolist(), s.diff().tolist())


Q(None, "Rolling Average", "Easy", "Smoothing noise",
  "Return the <code>k</code>-period trailing moving average (None until there are k values), rounded to 2.",
  [((SALES, 3), [None, None, 13.67, 16.33, 15.67, 16.33, 14.67, 17.67, 17.0, 18.0, 16.33, 20.0]), ((SALES[:4], 4), [None, None, None, 15.25])],
  ("Re-add each window, or slide a running sum.", "O(n)", "O(n)"),
  ("<code>s.rolling(k).mean()</code>.", "O(n)", "O(n)"),
  viz=(SALES, 3))


@B
def rolling_mean(values, k):
    out = []
    total = 0
    for i, v in enumerate(values):
        total += v
        if i >= k:
            total -= values[i - k]
        out.append(round(total / k, 2) if i >= k - 1 else None)
    return out


@O
def rolling_mean(values, k):
    return pd.Series(values).rolling(k).mean().round(2).tolist()


Q(None, "Exponential Moving Average", "Medium", "ewm",
  "Return the exponentially weighted average with smoothing <code>alpha</code>: e₀ = x₀, eₜ = αxₜ + (1 − α)eₜ₋₁ (rounded to 4).",
  [((SALES[:6], 0.5), [12.0, 13.5, 13.75, 16.875, 14.9375, 15.4688]), ((SALES[:6], 0.2), [12.0, 12.6, 12.88, 14.304, 14.0432, 14.4346])],
  ("Apply the recurrence in a loop.", "O(n)", "O(n)"),
  ("<code>s.ewm(alpha=alpha, adjust=False).mean()</code>.", "O(n)", "O(n)"),
  viz=(SALES[:6], 0.5))


@B
def ema(values, alpha):
    out = [float(values[0])]
    for x in values[1:]:
        out.append(alpha * x + (1 - alpha) * out[-1])
    return [round(v, 4) for v in out]


@O
def ema(values, alpha):
    return pd.Series(values, dtype=float).ewm(alpha=alpha, adjust=False).mean().round(4).tolist()


Q(None, "Baseline Forecasts", "Easy", "Naive, mean, seasonal naive",
  "Forecast the next <code>h</code> values with three baselines. Return <code>(naive, mean, seasonal naive)</code> lists, where the season length is <code>m</code>. Means are rounded to 2.",
  [((SALES, 4, 4), ([25, 25, 25, 25], [16.75, 16.75, 16.75, 16.75], [14, 18, 17, 25]))],
  ("Repeat the last value; repeat the average; repeat the last season.", "O(n + h)", "O(h)"),
  ("NumPy: <code>np.full</code>, <code>np.mean</code> and <code>np.resize</code> of the last season.", "O(n + h)", "O(h)"),
  viz=(SALES, 4, 4))


@B
def baselines(values, h, m):
    naive = [values[-1]] * h
    avg = round(sum(values) / len(values), 2)
    season = values[-m:]
    seasonal = [season[i % m] for i in range(h)]
    return (naive, [avg] * h, seasonal)


@O
def baselines(values, h, m):
    a = np.array(values)
    return (np.full(h, a[-1]).tolist(), np.full(h, round(a.mean(), 2)).tolist(), np.resize(a[-m:], h).tolist())


Q(None, "Forecast Error Metrics", "Easy", "MAE, RMSE, MAPE",
  "Return <code>(MAE, RMSE, MAPE %)</code> of <code>forecast</code> against <code>actual</code>, rounded to 2.",
  [(([20, 13, 16, 15], [22, 14, 18, 17]), (1.75, 1.8, 10.88))],
  ("Loop and accumulate absolute, squared and percentage errors.", "O(n)", "O(1)"),
  ("Vectorised NumPy expressions.", "O(n)", "O(n)"),
  viz=([20, 13, 16, 15], [22, 14, 18, 17]))


@B
def errors(actual, forecast):
    n = len(actual)
    ae = se = pe = 0
    for a, f in zip(actual, forecast):
        ae += abs(a - f)
        se += (a - f) ** 2
        pe += abs(a - f) / abs(a)
    return (round(ae / n, 2), round(math.sqrt(se / n), 2), round(pe / n * 100, 2))


@O
def errors(actual, forecast):
    a, f = np.array(actual, float), np.array(forecast, float)
    e = a - f
    return (round(np.abs(e).mean(), 2), round(np.sqrt((e ** 2).mean()), 2), round((np.abs(e) / np.abs(a)).mean() * 100, 2))


Q(None, "Which Baseline Wins?", "Medium", "Backtesting",
  "Hold out the last <code>h</code> values. Forecast them with naive, mean and seasonal-naive (season <code>m</code>) from the rest, and return the method names sorted by MAE (best first).",
  [((SEASONAL, 4, 4), ['seasonal', 'mean', 'naive']), ((SALES, 4, 4), ['seasonal', 'mean', 'naive'])],
  ("Compute each forecast and its MAE in loops.", "O(n)", "O(h)"),
  ("Put the forecasts in a dict of arrays and rank by vectorised MAE.", "O(n)", "O(h)"),
  viz=(SEASONAL, 4, 4))


@B
def best_baseline(values, h, m):
    train, test = values[:-h], values[-h:]
    fc = {"naive": [train[-1]] * h,
          "mean": [sum(train) / len(train)] * h,
          "seasonal": [train[-m:][i % m] for i in range(h)]}
    mae = {}
    for name, f in fc.items():
        mae[name] = sum(abs(a - b) for a, b in zip(test, f)) / h
    return sorted(mae, key=lambda k: mae[k])


@O
def best_baseline(values, h, m):
    a = np.array(values, float)
    train, test = a[:-h], a[-h:]
    fc = {"naive": np.full(h, train[-1]), "mean": np.full(h, train.mean()), "seasonal": np.resize(train[-m:], h)}
    return sorted(fc, key=lambda k: np.abs(test - fc[k]).mean())


Q(None, "Straight-Line Trend Forecast", "Easy", "Linear trend",
  "Fit y = a + b·t (t = 0, 1, 2, …) by least squares and forecast the next <code>h</code> points, rounded to 2.",
  [((SALES, 3), [20.95, 21.6, 22.25])],
  ("Slope = Σ(t − t̄)(y − ȳ) / Σ(t − t̄)².", "O(n)", "O(1)"),
  ("<code>np.polyfit(t, y, 1)</code> and <code>np.polyval</code>.", "O(n)", "O(h)"),
  viz=(SALES, 3))


@B
def trend_forecast(values, h):
    n = len(values)
    tm, ym = (n - 1) / 2, sum(values) / n
    b = sum((t - tm) * (y - ym) for t, y in enumerate(values)) / sum((t - tm) ** 2 for t in range(n))
    a = ym - b * tm
    return [round(a + b * t, 2) for t in range(n, n + h)]


@O
def trend_forecast(values, h):
    n = len(values)
    coef = np.polyfit(np.arange(n), values, 1)
    return np.round(np.polyval(coef, np.arange(n, n + h)), 2).tolist()


Q(None, "Seasonal Indices", "Medium", "Classical decomposition",
  "For season length <code>m</code>, estimate each position's seasonal effect: subtract a centred moving average (a 2×m average for even m), average the leftovers by position, then shift so they add to 0. Round to 2.",
  [((SEASONAL, 4), [-8.0, 1.5, 11.0, -4.5])],
  ("Compute the centred average by hand, then group leftovers by position in a list of lists.", "O(nm)", "O(n)"),
  ("<code>rolling(m, center=True)</code> twice, then <code>groupby(position).mean()</code>.", "O(n)", "O(n)"),
  viz=(SEASONAL, 4))


@B
def seasonal_index(values, m):
    n = len(values)
    half = m // 2
    buckets = [[] for _ in range(m)]
    for t in range(half, n - half):
        window = values[t - half:t + half + 1]
        trend = (sum(window) - window[0] / 2 - window[-1] / 2) / m
        buckets[t % m].append(values[t] - trend)
    idx = [sum(b) / len(b) for b in buckets]
    shift = sum(idx) / m
    return [round(i - shift, 2) for i in idx]


@O
def seasonal_index(values, m):
    s = pd.Series(values, dtype=float)
    trend = s.rolling(m).mean().rolling(2).mean().shift(-(m // 2))
    detr = (s - trend).dropna()
    idx = detr.groupby(detr.index % m).mean()
    return (idx - idx.mean()).round(2).tolist()


Q(None, "Autocorrelation at a Lag", "Medium", "Does it repeat?",
  "Return the correlation between the series and itself shifted by <code>lag</code> (pandas <code>autocorr</code>), rounded to 4.",
  [((SEASONAL, 4), 1.0), ((SEASONAL, 2), -0.8665)],
  ("Pearson r between values[lag:] and values[:-lag].", "O(n)", "O(n)"),
  ("<code>s.autocorr(lag)</code>.", "O(n)", "O(n)"),
  viz=(SEASONAL, 4))


@B
def autocorr(values, lag):
    x, y = values[lag:], values[:-lag]
    mx, my = sum(x) / len(x), sum(y) / len(y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    return round(sxy / math.sqrt(sxx * syy), 4)


@O
def autocorr(values, lag):
    return round(pd.Series(values, dtype=float).autocorr(lag), 4)


Q(None, "Find the Season Length", "Medium", "Peak autocorrelation",
  "Return the lag between 2 and n // 2 with the highest autocorrelation (smallest lag on ties).",
  [((SEASONAL,), 4), (([1, 5, 2, 1, 5, 2, 1, 5, 2, 1, 5, 2],), 3)],
  ("Compute each lag's correlation by formula and keep the best.", "O(n²)", "O(n)"),
  ("A dict of <code>s.autocorr(k)</code> and <code>max</code>.", "O(n²)", "O(n)"),
  viz=(SEASONAL,))


@B
def season_length(values):
    best, best_r = None, None
    for lag in range(2, len(values) // 2 + 1):
        x, y = values[lag:], values[:-lag]
        mx, my = sum(x) / len(x), sum(y) / len(y)
        r = sum((a - mx) * (b - my) for a, b in zip(x, y)) / math.sqrt(
            sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y))
        if best_r is None or r > best_r + 1e-12:
            best, best_r = lag, r
    return best


@O
def season_length(values):
    s = pd.Series(values, dtype=float)
    r = {k: s.autocorr(k) for k in range(2, len(s) // 2 + 1)}
    return max(r, key=lambda k: (round(r[k], 12), -k))


Q(None, "Walk-Forward Validation Splits", "Medium", "Never train on the future",
  "Return expanding-window folds for n points: each fold trains on everything before its test block of size <code>h</code>. Make <code>k</code> folds ending at the last point. Each fold is <code>(train length, test start, test end exclusive)</code>.",
  [((12, 3, 2), [(6, 6, 8), (8, 8, 10), (10, 10, 12)]), ((10, 2, 3), [(4, 4, 7), (7, 7, 10)])],
  ("Work backwards from the end in steps of h.", "O(k)", "O(k)"),
  ("sklearn's <code>TimeSeriesSplit(n_splits=k, test_size=h)</code>.", "O(k)", "O(k)"),
  viz=(12, 3, 2))


@B
def walk_forward(n, k, h):
    folds = []
    for i in range(k, 0, -1):
        start = n - i * h
        folds.append((start, start, start + h))
    return folds


@O
def walk_forward(n, k, h):
    from sklearn.model_selection import TimeSeriesSplit
    return [(len(tr), int(te[0]), int(te[-1]) + 1) for tr, te in TimeSeriesSplit(n_splits=k, test_size=h).split(np.zeros(n))]


Q(None, "Year-over-Year Change", "Easy", "Compare with the same season",
  "Monthly data with season <code>m</code>. Return the % change of each value vs m periods earlier (rounded to 1), starting from index m.",
  [((SEASONAL, 4), [20.0, 10.0, 6.7, 13.3, 16.7, 9.1, 6.2, 11.8])],
  ("Index arithmetic: (x[t] − x[t−m]) / x[t−m].", "O(n)", "O(n)"),
  ("<code>s.pct_change(periods=m)</code>.", "O(n)", "O(n)"),
  viz=(SEASONAL, 4))


@B
def yoy(values, m):
    return [round((values[t] - values[t - m]) / values[t - m] * 100, 1) for t in range(m, len(values))]


@O
def yoy(values, m):
    return pd.Series(values, dtype=float).pct_change(periods=m).mul(100).round(1).dropna().tolist()


Q(None, "Flag Anomalies", "Medium", "Rolling z-score",
  "Flag index t when its value is more than <code>k</code> standard deviations from the mean of the <code>w</code> values before it (sample std). Return the flagged indexes.",
  [(([10, 11, 10, 12, 11, 30, 11, 10, 12, 2, 11], 4, 3), [5])],
  ("For each t, compute the mean and std of the previous window by hand.", "O(nw)", "O(w)"),
  ("<code>rolling(w).mean().shift(1)</code> and <code>rolling(w).std().shift(1)</code> so today isn't in its own baseline.", "O(n)", "O(n)"),
  viz=([10, 11, 10, 12, 11, 30, 11, 10, 12, 2, 11], 4, 3))


@B
def anomalies(values, w, k):
    flags = []
    for t in range(w, len(values)):
        win = values[t - w:t]
        m = sum(win) / w
        sd = math.sqrt(sum((v - m) ** 2 for v in win) / (w - 1))
        if abs(values[t] - m) > k * sd:
            flags.append(t)
    return flags


@O
def anomalies(values, w, k):
    s = pd.Series(values, dtype=float)
    mean, sd = s.rolling(w).mean().shift(1), s.rolling(w).std().shift(1)
    return s.index[(s - mean).abs() > k * sd].tolist()


Q(None, "Returns and Compound Growth", "Easy", "pct_change · cumprod",
  "From prices, return <code>(daily returns %, total return %)</code> rounded to 2, where the total compounds the daily returns.",
  [(([100, 110, 99, 108.9],), ([10.0, -10.0, 10.0], 8.9))],
  ("A loop for the returns and a running product.", "O(n)", "O(n)"),
  ("<code>pct_change()</code> and <code>(1 + r).prod() − 1</code>.", "O(n)", "O(n)"),
  viz=([100, 110, 99, 108.9],))


@B
def returns(prices):
    r = [(prices[i] / prices[i - 1] - 1) for i in range(1, len(prices))]
    growth = 1.0
    for x in r:
        growth *= 1 + x
    return ([round(x * 100, 2) for x in r], round((growth - 1) * 100, 2))


@O
def returns(prices):
    r = pd.Series(prices, dtype=float).pct_change().dropna()
    return ((r * 100).round(2).tolist(), round(((1 + r).prod() - 1) * 100, 2))


Q(None, "Average by Day of the Week", "Easy", "Calendar features",
  "Return the average value for each weekday name that appears, in Monday-to-Sunday order, rounded to 2.",
  [((["2026-03-02", "2026-03-03", "2026-03-09", "2026-03-10", "2026-03-14"], [10, 20, 14, 22, 40]), {'Monday': 12.0, 'Tuesday': 21.0, 'Saturday': 40.0})],
  ("<code>date.weekday()</code> and a dict of lists.", "O(n)", "O(7)"),
  ("<code>groupby(index.day_of_week)</code>, then map to names.", "O(n)", "O(7)"),
  viz=(["2026-03-02", "2026-03-03", "2026-03-09", "2026-03-10", "2026-03-14"], [10, 20, 14, 22, 40]))


@B
def by_weekday(days, values):
    names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    groups = {}
    for d, v in zip(days, values):
        groups.setdefault(date.fromisoformat(d).weekday(), []).append(v)
    return {names[k]: round(sum(g) / len(g), 2) for k, g in sorted(groups.items())}


@O
def by_weekday(days, values):
    s = pd.Series(values, index=pd.to_datetime(days), dtype=float)
    g = s.groupby(s.index.day_of_week).mean().round(2)
    names = pd.Series(s.index.day_name(), index=s.index.day_of_week).groupby(level=0).first()
    return {names[k]: v for k, v in g.items()}


Q(None, "Turn a Series into a Supervised Dataset", "Medium", "Lag features",
  "Build rows of the previous <code>p</code> values (oldest first) as X, with the next value as y. Return <code>(X, y)</code>.",
  [((SALES[:6], 3), ([[12, 15, 14], [15, 14, 20], [14, 20, 13]], [20, 13, 16]))],
  ("Slide a window with a loop.", "O(np)", "O(np)"),
  ("<code>sliding_window_view</code> gives every window at once.", "O(np)", "O(np)"),
  viz=(SALES[:6], 3))


@B
def supervised(values, p):
    X, y = [], []
    for t in range(p, len(values)):
        X.append(values[t - p:t])
        y.append(values[t])
    return (X, y)


@O
def supervised(values, p):
    a = np.array(values)
    X = np.lib.stride_tricks.sliding_window_view(a[:-1], p)
    return (X.tolist(), a[p:].tolist())


Q(None, "Autoregressive Forecast AR(1)", "Hard", "Regress on the past",
  "Fit xₜ = c + φ·xₜ₋₁ by least squares and forecast the next <code>h</code> values recursively. Return <code>(c, φ, forecasts)</code>, rounded to 4.",
  [((SALES, 3), (21.5296, -0.2717, [14.7362, 17.5253, 16.7673]))],
  ("Simple regression formulas on (x[t−1], x[t]) pairs, then a loop.", "O(n + h)", "O(n)"),
  ("<code>np.linalg.lstsq</code> on a design matrix [1, xₜ₋₁].", "O(n + h)", "O(n)"),
  viz=(SALES, 3))


@B
def ar1(values, h):
    x, y = values[:-1], values[1:]
    mx, my = sum(x) / len(x), sum(y) / len(y)
    phi_ = sum((a - mx) * (b - my) for a, b in zip(x, y)) / sum((a - mx) ** 2 for a in x)
    c = my - phi_ * mx
    out, last = [], values[-1]
    for _ in range(h):
        last = c + phi_ * last
        out.append(round(last, 4))
    return (round(c, 4), round(phi_, 4), out)


@O
def ar1(values, h):
    a = np.array(values, float)
    A = np.column_stack([np.ones(len(a) - 1), a[:-1]])
    (c, phi_), *_ = np.linalg.lstsq(A, a[1:], rcond=None)
    out, last = [], a[-1]
    for _ in range(h):
        last = c + phi_ * last
        out.append(round(last, 4))
    return (round(c, 4), round(phi_, 4), out)


Q(None, "Tune the Smoothing Factor", "Medium", "Simple exponential smoothing",
  "With simple exponential smoothing, the forecast for step t is the smoothed value at t − 1. For each alpha in <code>alphas</code> add up the squared one-step-ahead errors (from t = 1). Return <code>(best alpha, its SSE)</code>, SSE rounded to 2.",
  [((SALES, [0.1, 0.3, 0.5, 0.9]), (0.3, 192.3)), (([10, 12, 14, 16, 18, 20], [0.2, 0.5, 0.9]), (0.9, 23.64))],
  ("Run the recurrence for each alpha and sum the errors.", "O(n·a)", "O(1)"),
  ("<code>ewm(alpha, adjust=False).mean().shift(1)</code> is the forecast series; subtract and square.", "O(n·a)", "O(n)"),
  viz=(SALES, [0.1, 0.3, 0.5, 0.9]))


@B
def tune_alpha(values, alphas):
    best = None
    for alpha in alphas:
        level = values[0]
        sse = 0
        for x in values[1:]:
            sse += (x - level) ** 2
            level = alpha * x + (1 - alpha) * level
        if best is None or sse < best[1]:
            best = (alpha, sse)
    return (best[0], round(best[1], 2))


@O
def tune_alpha(values, alphas):
    s = pd.Series(values, dtype=float)
    sse = {a: ((s - s.ewm(alpha=a, adjust=False).mean().shift(1)) ** 2).sum() for a in alphas}
    best = min(sse, key=sse.get)
    return (best, round(sse[best], 2))
