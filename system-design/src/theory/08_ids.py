from lib import *

THEORY("ID schemes compared", """
<table>
<tr><th>Scheme</th><th>Size</th><th>Sortable</th><th>Coordination</th></tr>
<tr><td>Auto-increment</td><td>64 bit</td><td>yes</td><td>one database</td></tr>
<tr><td>UUIDv4</td><td>128 bit</td><td>no</td><td>none</td></tr>
<tr><td>Snowflake</td><td>64 bit</td><td>by time</td><td>unique machine ids</td></tr>
<tr><td>ULID / UUIDv7</td><td>128 bit</td><td>by time</td><td>none</td></tr>
</table>
""")

FAQ("301 or 302 for redirects?", "<p>301 is permanent and cached by browsers, so repeat clicks never reach you — less load but no analytics. 302 (or 307) is temporary, so every click is counted.</p>")
FAQ("How do you avoid two servers generating the same short code?", "<p>Use a central counter with ranges per server, a key-generation service with pre-allocated keys, or hash with a uniqueness check (a conditional insert that fails if the code exists).</p>")
FAQ("How would you scale reads for a shortener?", "<p>Cache hot codes in Redis and at the CDN edge, use read replicas or a key-value store sharded by code, and keep the redirect path free of synchronous analytics writes.</p>")
FAQ("Why not use UUIDs as primary keys everywhere?", "<p>Random UUIDs scatter inserts across the B-tree, causing page splits and poor cache use. Time-ordered IDs (UUIDv7, ULID, Snowflake) insert near the end of the index.</p>")
FAQ("What if Snowflake's clock goes backwards?", "<p>Refuse to issue ids or wait until the clock passes the last timestamp, or keep using the last timestamp with the sequence. Never issue ids with an earlier timestamp.</p>")
FAQ("Why shouldn't public ids be sequential?", "<p>They reveal volumes (orders per day) and make enumeration attacks easy. Expose random or encoded ids and keep sequential keys internal.</p>")
