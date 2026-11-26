from lib import *

LESSON("Basics", "Design a URL shortener", """
<p><b>Requirements</b>: shorten a long URL, redirect fast, optional custom alias and expiry, click analytics. Reads outnumber writes ~100:1.</p>
<pre><code class="py">POST /v1/links {long_url, alias?, ttl?} → 201 {code}
GET  /{code}  → 301/302 Location: long_url</code></pre>
<p><b>High level</b>: stateless API servers → cache (Redis, hot codes) → key-value store (code → long URL), sharded by code. Analytics go through a queue so redirects stay fast. A 7-character base62 code gives 3.5 trillion links.</p>
<p><b>Deep dives</b>: how to generate codes (below), 301 vs 302 (302 keeps every click visible for analytics), expiry, abuse (rate limits, malware checks).</p>
""", practice=["Napkin Maths for a Shortener", "How Long Will the Codes Last?", "Validate Custom Aliases", "Expire Old Links", "Click Analytics", "Canonicalise URLs Before Shortening"])

LESSON("Core", "Generating short codes", """
<table>
<tr><th>Approach</th><th>Pros</th><th>Cons</th></tr>
<tr><td>Counter + base62</td><td>no collisions, short</td><td>needs a shared counter; guessable</td></tr>
<tr><td>Counter ranges per server</td><td>no per-request coordination</td><td>ids out of global order; lost ranges on crash</td></tr>
<tr><td>Hash of URL (first k chars)</td><td>same URL → same code</td><td>collisions to detect and retry</td></tr>
<tr><td>Key-generation service</td><td>pre-made random keys, fast</td><td>another service; crash wastes batches</td></tr>
</table>
<p>A <b>Bloom filter</b> answers "is this code taken?" in memory: "no" is certain, "maybe" needs a database check.</p>
""", practice=["Base62 Encode", "Base62 Decode", "Hash, Then Handle Collisions", "Hand Out ID Ranges", "A Key-Generation Service", "A Bloom Filter for Taken Codes", "Sequential IDs Leak Your Numbers"])

LESSON("Core", "Unique IDs at scale", """
<p>Auto-increment ids need one database. Alternatives:</p>
<ul>
<li><b>UUIDv4</b>: 122 random bits, no coordination, but random order hurts B-tree index locality.</li>
<li><b>Snowflake</b>: 41-bit ms timestamp + 10-bit machine + 12-bit sequence in 64 bits — roughly time-ordered, 4096 ids per ms per machine. Machine ids must be unique, and the clock must never go backwards.</li>
<li><b>ULID / UUIDv7</b>: timestamp prefix + randomness — sortable strings that index well.</li>
</ul>
""", practice=["Build a Snowflake ID", "Decode a Snowflake ID", "When the Sequence Runs Out", "The Clock Went Backwards", "Machine IDs Across Data Centres", "Time-Sortable String IDs", "When Do Random IDs Collide?"])


@LD
def snowflake_demo():
    epoch = 1_700_000_000_000
    ms, machine, seq = 1_700_000_123_456, 7, 3
    sid = (ms - epoch) << 22 | machine << 12 | seq
    print("id:", sid)
    print("timestamp:", (sid >> 22) + epoch, "machine:", (sid >> 12) & 1023, "sequence:", sid & 4095)
