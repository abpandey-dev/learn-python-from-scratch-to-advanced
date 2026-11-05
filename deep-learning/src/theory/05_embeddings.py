from lib import *

THEORY("Text representations compared", """
<table><tr><th>Method</th><th>Size</th><th>Knows meaning?</th><th>Good for</th></tr>
<tr><td>One-hot</td><td>vocabulary</td><td>no</td><td>teaching</td></tr>
<tr><td>Bag of words / TF-IDF</td><td>vocabulary, sparse</td><td>no</td><td>keyword search, simple classifiers</td></tr>
<tr><td>Word2vec / GloVe</td><td>about 300</td><td>one sense per word</td><td>light features</td></tr>
<tr><td>Transformer embeddings</td><td>hundreds to thousands</td><td>depends on context</td><td>semantic search, RAG</td></tr></table>
""")

THEORY("Tokeniser facts for LLM work", """
<ul><li>Pricing and context limits are in tokens.</li>
<li>4 characters per token is a rough English estimate. Languages other than English and code can differ considerably.</li>
<li>Use a model's own tokeniser or token-counting API when accuracy matters.</li>
<li>Token ids aren't portable: a model must use the tokeniser it was trained with.</li>
<li>Decide deliberately how to truncate. Cutting the end of a document might remove what you need.</li></ul>
""")

THEORY("Formulas", """
<table><tr><th>Quantity</th><th>Formula</th></tr>
<tr><td>TF-IDF</td><td>(count / length) × ln(N / df)</td></tr>
<tr><td>PMI</td><td>ln(c·N / (x·y))</td></tr>
<tr><td>Cosine</td><td>a·b / (‖a‖·‖b‖)</td></tr>
<tr><td>Negative sampling</td><td>−ln σ(c·p) − Σ ln σ(−c·n)</td></tr>
<tr><td>Table size</td><td>vocabulary × dimension</td></tr></table>
<p>TF-IDF has many variants, so libraries such as scikit-learn give somewhat different numbers.</p>
""")

FAQ("What is an embedding?", "<p>A short learned vector for a token or text, placed so that similar things have similar vectors.</p>")
FAQ("Why subword tokens rather than words?", "<p>They keep the vocabulary manageable and let the model handle new words by combining known pieces.</p>")
FAQ("Why does TF-IDF give 'the' zero?", "<p>It appears in every document, so ln(N / df) = ln 1 = 0. It can't distinguish one document from another.</p>")
FAQ("Are embeddings the same as a model's token ids?", "<p>No. Ids are arbitrary labels with no meaning. Embeddings are the learned vectors those ids look up.</p>")
FAQ("Should I normalise embeddings?", "<p>For cosine search, yes. Then a dot product equals cosine similarity, and it's quick to compute at scale.</p>")
