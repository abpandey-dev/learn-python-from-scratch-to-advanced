from lib import *

LESSON("Basics", "Logging instead of print", """
<p><code>print</code> has no levels, no timestamps, and can't be turned down or sent elsewhere. The <code>logging</code> module gives every message a <b>level</b>, a <b>logger name</b> (usually the module) and a <b>format</b>, and lets you decide in one place where logs go.</p>
<pre><code class="py">import logging
log = logging.getLogger(__name__)

def charge(order):
    log.debug("charging order %s", order.id)        # lazy formatting: cheap if DEBUG is off
    try:
        gateway.charge(order.total)
    except GatewayTimeout:
        log.warning("gateway timeout for order %s, retrying", order.id)
        raise
    log.info("charged order %s", order.id)

# in the entry point only
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-8s %(name)s: %(message)s")
logging.getLogger("urllib3").setLevel(logging.WARNING)   # quiet a chatty library</code></pre>
""", practice=["Which Messages Get Logged?", "Format Log Lines", "The Logger Hierarchy", "Rotate Log Files by Size"])

LESSON("Core", "Logs that help at 3 a.m.", """
<ul>
<li><b>Structured (JSON) logs</b> let you filter by field: <code>level=ERROR and order_id=42</code>.</li>
<li>Put a <b>request id</b> on every line and pass it to every service you call — then one search shows the whole journey.</li>
<li><b>Never log secrets or personal data</b>: redact passwords, tokens, emails and card numbers before they're written.</li>
<li>Log exceptions with <code>log.exception</code> (it adds the traceback), and wrap low-level errors with context using <code>raise AppError(...) from e</code>.</li>
<li>At high volume, <b>sample</b> routine logs but keep every warning and error.</li>
</ul>
<pre><code class="py">import structlog
log = structlog.get_logger()
log.info("order_placed", order_id=42, amount=499.0, request_id=req_id)
# {"event": "order_placed", "order_id": 42, "amount": 499.0, "request_id": "r-7", "level": "info"}</code></pre>
""", practice=["Structured JSON Logs", "Follow a Request Across Services", "Redact Personal Data From Logs", "Wrap Errors With Context", "Sample Logs, Keep Every Error", "Group Errors Like Sentry"])

LESSON("Core", "Metrics: numbers over time", """
<p>Logs tell you what happened to one request; <b>metrics</b> tell you how the whole system is doing. Prometheus-style metrics come in three kinds: <b>counters</b> (only go up: requests, errors — graph their <i>rate</i>), <b>gauges</b> (go up and down: queue depth, memory) and <b>histograms</b> (distributions: latency, estimated into percentiles).</p>
<pre><code class="py">from prometheus_client import Counter, Histogram, start_http_server
REQUESTS = Counter("http_requests_total", "Requests", ["route", "status"])
LATENCY = Histogram("http_request_seconds", "Latency", buckets=[.025, .05, .1, .25, .5, 1])

with LATENCY.time():
    handle(request)
REQUESTS.labels(route="/orders", status="200").inc()
start_http_server(9100)        # Prometheus scrapes /metrics

# PromQL
rate(http_requests_total{status=~"5.."}[5m])
histogram_quantile(0.95, rate(http_request_seconds_bucket[5m]))</code></pre>
""", practice=["Error Rate per Minute", "A Prometheus Histogram", "Estimate a Percentile From Buckets", "Rate From a Counter With Resets"])

LESSON("Advanced", "Running safely in production", """
<ul>
<li><b>Validate config at startup</b> and crash immediately on bad settings.</li>
<li><b>Retry</b> only transient errors (timeouts, connection resets), with backoff and a limit.</li>
<li>Expose a <b>/health</b> endpoint that load balancers and Kubernetes can probe; distinguish "down" from "degraded".</li>
<li>Ship risky changes behind <b>feature flags</b> and roll out by percentage.</li>
<li><b>Alert</b> on symptoms users feel, with cooldowns so one problem pages once; track <b>uptime</b> against your SLO.</li>
</ul>
""", practice=["Validate Configuration at Startup", "Retry With Backoff", "Aggregate Health Checks", "Roll Out a Feature Flag", "Alert Without Spamming", "Uptime From Health Checks"])
