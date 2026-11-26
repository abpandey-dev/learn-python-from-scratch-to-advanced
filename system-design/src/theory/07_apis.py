from lib import *

THEORY("REST vs gRPC vs GraphQL", """
<table>
<tr><th></th><th>REST</th><th>gRPC</th><th>GraphQL</th></tr>
<tr><td>Format</td><td>JSON over HTTP</td><td>Protobuf over HTTP/2</td><td>JSON, one endpoint</td></tr>
<tr><td>Best for</td><td>public APIs</td><td>internal, low latency, streaming</td><td>many client shapes, mobile</td></tr>
<tr><td>Caching</td><td>HTTP caching works</td><td>custom</td><td>harder</td></tr>
</table>
""")

FAQ("Design a rate limiter.", "<p>Clarify: per user or IP, limits, hard or soft. Put it in the gateway; use a token bucket or sliding window counter stored in Redis with atomic operations (Lua or INCR + EXPIRE); return 429 with Retry-After and rate-limit headers; fail open if Redis is down for non-critical limits.</p>")
FAQ("Why cursor pagination?", "<p>It uses the index to jump straight to the next page (constant cost), and inserts or deletes don't shift pages, so nothing is skipped or repeated.</p>")
FAQ("How do you make POST safe to retry?", "<p>Require an Idempotency-Key header; store key → response atomically with the change; return the stored response for repeats and reject reuse with a different body.</p>")
FAQ("What does a circuit breaker solve?", "<p>It stops a failing dependency from tying up threads and connections with doomed calls, returns errors or fallbacks fast, and periodically tests whether the dependency has recovered.</p>")
FAQ("How do you version an API?", "<p>Put the major version in the path (/v1) or a header, make additive changes without a new version, and deprecate old versions with notice before returning 410.</p>")
FAQ("Polling, long polling, SSE or WebSockets?", "<p>Polling is simplest but wasteful; long polling holds the request until data arrives; SSE is one-way server push over HTTP; WebSockets are two-way, for chat and games.</p>")
