from lib import *

LESSON("Basics", "Designing an API", """
<p>In an interview, write the API right after requirements — it pins down what the system does.</p>
<pre><code class="py">POST   /v1/orders               body {items, address}  Idempotency-Key: 7f3c…   → 201 {order_id}
GET    /v1/orders/{id}                                                         → 200 / 404
GET    /v1/users/{id}/orders?limit=20&amp;cursor=eyJpZCI6MTAyfQ                → 200 {items, next_cursor}
PATCH  /v1/orders/{id}          body {status}                                  → 200 / 409</code></pre>
<ul>
<li>Nouns for resources, HTTP verbs for actions, plural paths, a version in the path or a header.</li>
<li>Right status codes: 2xx success, 4xx the client's fault, 5xx yours; 429 with <code>Retry-After</code> when throttled.</li>
<li>REST for public CRUD APIs, gRPC for fast internal service-to-service calls, GraphQL when clients need flexible shapes, WebSockets/SSE for server push.</li>
</ul>
""", practice=["Pick the Status Code", "Safe and Idempotent Methods", "Route by API Version", "Polling vs Push"])

LESSON("Core", "Pagination, idempotency and caching", """
<ul>
<li><b>Offset</b> pagination (<code>LIMIT 20 OFFSET 4000</code>) is simple but slow deep down and skips or repeats rows as data changes. <b>Cursor/keyset</b> pagination (<code>WHERE (created_at, id) &lt; cursor</code>) is stable and uses the index.</li>
<li><b>Idempotency keys</b> make POST safe to retry: store the key with the response and replay it.</li>
<li><b>ETags</b> let clients revalidate: send <code>If-None-Match</code>, get 304 with no body if nothing changed.</li>
<li>Reduce round trips: batch endpoints, or parallel calls with a concurrency limit.</li>
</ul>
""", practice=["Offset vs Cursor Pagination", "Keyset Pagination With Ties", "Idempotency Keys", "Conditional GET With ETags", "Chatty vs Batched vs Parallel Calls"])

LESSON("Core", "Rate limiting", """
<p>Rate limits protect your service from abuse and from one client starving the rest. Limit per user, API key or IP, usually at the gateway, with counters in Redis so all gateway nodes share them.</p>
<table>
<tr><th>Algorithm</th><th>Pros</th><th>Cons</th></tr>
<tr><td>Fixed window</td><td>one counter, simple</td><td>2× burst at window edges</td></tr>
<tr><td>Sliding log</td><td>exact</td><td>stores every timestamp</td></tr>
<tr><td>Sliding counter</td><td>two counters, smooth</td><td>approximate</td></tr>
<tr><td>Token bucket</td><td>allows controlled bursts</td><td>two values per client</td></tr>
<tr><td>Leaky bucket</td><td>perfectly smooth output</td><td>bursts are dropped or queued</td></tr>
</table>
""", practice=["Fixed-Window Rate Limiter", "The Window-Boundary Burst", "Sliding-Window Log", "Sliding-Window Counter", "Token Bucket", "Leaky Bucket", "Per-User Quotas"])


@LD
def bucket_demo():
    tokens, last, cap, rate = 3, 0, 3, 1
    for t in [0, 0, 0, 0, 0.5, 1.5, 2]:
        tokens = min(cap, tokens + (t - last) * rate); last = t
        ok = tokens >= 1
        tokens -= ok
        print(f"t={t:<4} {'allowed' if ok else 'rejected (429)'}  tokens left={tokens:.1f}")


LESSON("Advanced", "Resilience at the edge", """
<ul>
<li><b>Deadlines</b>: give every request a total time budget and pass it downstream; retries must fit inside it.</li>
<li><b>Circuit breakers</b> stop calling a failing dependency for a while, so you fail fast and give it room to recover.</li>
<li>An <b>API gateway</b> handles cross-cutting work: authentication, routing, rate limits, TLS, request logging.</li>
<li><b>Webhooks</b> push events to customers; sign them with HMAC so receivers can verify the sender, and retry with backoff.</li>
</ul>
""", practice=["Retries Within a Deadline", "A Circuit Breaker", "An API Gateway", "Sign Webhook Payloads (HMAC)"])
