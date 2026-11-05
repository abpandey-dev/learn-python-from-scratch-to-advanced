from lib import *
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


LESSON("Basics", "From text to numbers: tokens", """
<p>Neural networks need numbers. The journey from text is always the same:</p>
<p style="text-align:center"><b>text → tokens → ids → vectors</b></p>
<p>What counts as a token is a real design decision:</p>
<table><tr><th>Level</th><th>"unhappily" becomes</th><th>Vocabulary</th><th>Weakness</th></tr>
<tr><td>Characters</td><td>u, n, h, a, p, p, i, l, y</td><td>tiny (about 100)</td><td>long sequences; has to learn spelling first</td></tr>
<tr><td>Words</td><td>unhappily</td><td>huge</td><td>any unseen word is unknown</td></tr>
<tr><td>Subwords</td><td>un, happ, ily</td><td>tens of thousands</td><td>splits can look odd</td></tr></table>
<p>Modern LLMs use subwords, because a new word can still be built from known pieces.</p>
<p><b>A vocabulary by hand.</b> Tokens b, a, b, c, a, b with min_count = 2: a appears 2 times, b 3 times, c once, so c is dropped.</p>
<p>The vocabulary is &lt;pad&gt; = 0, &lt;unk&gt; = 1, a = 2, b = 3. Encoding a, z, b gives <b>[2, 1, 3]</b>, since z becomes unknown. Special tokens matter: padding fills batches, and "unknown" stops unseen words crashing the code.</p>
<p>A simple word tokeniser turns "Hello, World! It's 2024." into hello, world, it, s, 2024. Notice "It's" split in two, and the punctuation gone. Every choice loses something.</p>
""", practice=["Word Tokeniser", "Build a Vocabulary", "Encode With Unknowns", "Truncate and Pad to a Fixed Length"])


LESSON("Core", "Byte-pair encoding, by hand", """
<p><b>BPE</b> is the method behind most LLM tokenisers. It learns subwords directly from data:</p>
<ol><li>Start with every word split into characters.</li><li>Count neighbouring pairs across the corpus.</li><li>Merge the most frequent pair into one token.</li><li>Repeat until the vocabulary is the size you want.</li></ol>
<p>Words: low, lower, newest, widest.</p>
<p><b>Round 1:</b> Pair counts include l-o: 2, o-w: 2, w-e: 2, e-s: 2, s-t: 2, all tied. Breaking ties alphabetically, we merge <b>e + s → es</b>.</p>
<p><b>Round 2:</b> Now es-t appears twice, and it's the alphabetically first of the top pairs. Merge <b>es + t → est</b>.</p>
<p><b>Round 3:</b> Merge <b>l + o → lo</b>.</p>
<table><tr><th>Word</th><th>Start</th><th>After 3 merges</th></tr>
<tr><td>low</td><td>l o w</td><td>lo w</td></tr><tr><td>lower</td><td>l o w e r</td><td>lo w e r</td></tr>
<tr><td>newest</td><td>n e w e s t</td><td>n e w est</td></tr><tr><td>widest</td><td>w i d e s t</td><td>w i d est</td></tr></table>
<p>It has discovered "est" as a useful ending, without being told about English. To tokenise new text, you replay the merges in the same order. An unseen word like "slowest" still works, built from known pieces.</p>
<p>Real tokenisers differ in details (real tie-breaking usually isn't alphabetical, for example), and the same text can be a different number of tokens under different tokenisers.</p>
<p><b>Why you should care as an LLM developer:</b></p>
<ul><li><b>You're billed and limited by tokens</b>, not characters. English averages roughly 4 characters per token, so "Hello there" (11 characters) is about 3. That's only a quick guess; use your provider's token counter for real limits.</li>
<li><b>Models see tokens, not letters.</b> That's one reason counting the letters in a word can be surprisingly hard for them.</li></ul>
""", practice=["BPE: Most Frequent Pair", "BPE: Apply a Merge", "BPE: Train n Merges", "Rough Token Estimate"])


LESSON("Core", "Bag of words and TF-IDF", """
<p>Before embeddings, there were counts. They're still useful: search and RAG both rely on them, as you'll see later.</p>
<p>Three documents: "the cat sat", "the dog sat", "the dog ran fast".</p>
<table><tr><th></th><th>cat</th><th>dog</th><th>fast</th><th>ran</th><th>sat</th><th>the</th></tr>
<tr><td>Doc 0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>1</td></tr>
<tr><td>Doc 1</td><td>0</td><td>1</td><td>0</td><td>0</td><td>1</td><td>1</td></tr>
<tr><td>Doc 2</td><td>0</td><td>1</td><td>1</td><td>1</td><td>0</td><td>1</td></tr></table>
<p>But "the" tells you nothing, since it's everywhere. <b>TF-IDF</b> rewards words that are frequent here but rare overall:</p>
<p style="text-align:center"><b>tf-idf = (count ÷ doc length) × ln(documents ÷ documents containing it)</b></p>
<table><tr><th>Word, doc</th><th>tf</th><th>idf</th><th>Score</th></tr>
<tr><td>"cat", doc 0</td><td>1/3</td><td>ln(3/1) = 1.0986</td><td><b>0.3662</b></td></tr>
<tr><td>"dog", doc 2</td><td>1/4</td><td>ln(3/2) = 0.4055</td><td><b>0.1014</b></td></tr>
<tr><td>"the", doc 0</td><td>1/3</td><td>ln(3/3) = 0</td><td><b>0</b></td></tr></table>
<p>The rare word gets the highest score, and the universal one gets exactly zero.</p>
<p><b>The limitation:</b> "car" and "automobile" are as different here as "car" and "banana", because each word is just a separate column. It knows nothing about meaning. Embeddings fix that.</p>
""", practice=["Bag of Words", "TF-IDF"])


LESSON("Core", "Embeddings: a learned table of vectors", """
<p>A one-hot vector for 50,000 words is 50,000 numbers long, and every pair of words is equally far apart. An <b>embedding table</b> replaces this with a short, learned vector per token:</p>
<pre><code class="py">E = [[0.1, 0.2],     # id 0
     [0.3, 0.4],     # id 1
     [0.5, 0.6]]     # id 2

ids [2, 0, 2]  →  [[0.5, 0.6], [0.1, 0.2], [0.5, 0.6]]</code></pre>
<p>That's all an embedding layer is: looking up rows. It's equivalent to multiplying a one-hot vector by the table, but much faster. The numbers start random and are trained with the rest of the model.</p>
<p><b>Cost:</b> vocabulary × dimension. With 50,000 × 768 that's 38,400,000 parameters, or <b>153.6 MB</b> at 4 bytes each. It's often a large fraction of a small model.</p>
<p><b>The payoff</b> is that similar words end up with similar vectors, so you can measure meaning with cosine similarity. With the small table in the practice questions:</p>
<ul><li>king = (0.9, 0.8, 0.1), man = (0.5, 0.9, 0.1): 1.18 / (1.2083 × 1.0344) = <b>0.944</b>.</li>
<li>king and queen = (0.9, 0.1, 0.8): 0.97 / 1.46 = <b>0.664</b>.</li></ul>
<p>In this toy table, the second dimension acts like "male". Real dimensions don't usually have such neat meanings.</p>
<p><b>Analogies:</b> king − man + woman = (0.9, 0, 0.9). Its cosine with queen is <b>0.995</b>, the closest among the remaining words. A caveat: analogy code excludes the input words, and in real embeddings the nearest result is often just "king" without that exclusion. So analogies are an appealing demo, not proof that the model understands relations.</p>
""", practice=["Embedding Lookup", "Embedding Table Size", "Most Similar Vectors", "Word Analogy"])


LESSON("Core", "You shall know a word by its neighbours", """
<p>How can a machine learn meaning with no dictionary? From one observation: <b>words that appear in similar contexts have similar meanings</b>. "I drank a cup of ___" tells you the gap is a drink.</p>
<p><b>Counting method.</b> Count how often words appear near one another. For a, b, a, c with window 1:</p>
<table><tr><th></th><th>a</th><th>b</th><th>c</th></tr><tr><th>a</th><td>0</td><td>2</td><td>1</td></tr><tr><th>b</th><td>2</td><td>0</td><td>0</td></tr><tr><th>c</th><td>1</td><td>0</td><td>0</td></tr></table>
<p>But common words dominate raw counts. <b>Pointwise mutual information</b> asks whether a pair appears more than chance would predict:</p>
<p style="text-align:center"><b>PMI = ln( P(x, y) / (P(x)·P(y)) )</b></p>
<p>With x seen 20 times, y 30 times and N = 300 pairs:</p>
<ul><li>Together 10 times: ln(10·300 / (20·30)) = ln 5 = <b>1.609</b>: a real association.</li>
<li>Together 2 times: ln(2·300 / 600) = ln 1 = <b>0</b>: exactly what chance predicts.</li></ul>
<p>Keep the positive PMI values and compress the table with SVD, and each row becomes a compact word vector. The chart does this on eight short sentences, and shows the similarity of the resulting vectors. Cat and dog score high, as do car and truck, while pairs across those groups score low, though no one told it those categories. The corpus is tiny and built to make the pattern clear, so this demonstrates the idea and isn't a useful model.</p>
""", practice=["Co-occurrence Matrix", "Pointwise Mutual Information"])


@LD
def word_map():
    sentences = ["the cat drinks milk", "the dog drinks water", "the cat eats fish", "the dog eats meat",
                 "the car needs fuel", "the truck needs fuel", "the car uses road", "the truck uses road"]
    words = sorted({w for s in sentences for w in s.split()})
    index = {w: i for i, w in enumerate(words)}
    counts = np.zeros((len(words), len(words)))
    for s in sentences:
        tokens = s.split()
        for i, t in enumerate(tokens):
            for j in range(max(0, i - 2), min(len(tokens), i + 3)):
                if i != j:
                    counts[index[t], index[tokens[j]]] += 1
    total = counts.sum()
    row = counts.sum(axis=1, keepdims=True)
    with np.errstate(divide="ignore"):
        pmi = np.log(counts * total / (row @ row.T))
    ppmi = np.maximum(pmi, 0)
    U, S, _ = np.linalg.svd(ppmi)
    vectors = U[:, :3] * S[:3]
    show = ["cat", "dog", "car", "truck"]
    picked = vectors[[index[w] for w in show]]
    unit = picked / np.linalg.norm(picked, axis=1, keepdims=True)
    similarity = unit @ unit.T
    print(similarity.round(2))
    fig, ax = plt.subplots(figsize=(3.6, 3.2))
    ax.imshow(similarity, cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(range(4), show)
    ax.set_yticks(range(4), show)
    for r in range(4):
        for c in range(4):
            ax.text(c, r, f"{similarity[r, c]:.2f}", ha="center", va="center", fontsize=9,
                    color="white" if similarity[r, c] > 0.6 else "black")
    ax.set_title("Cosine similarity, from counts alone", fontsize=9)


LESSON("Core", "Word2vec: skip-gram with negative sampling", """
<p>Instead of counting and compressing, <b>word2vec</b> learns vectors by making a simple prediction: given a word, is this other word nearby?</p>
<p><b>Training pairs:</b> for "the cat sat" with window 1: (the, cat), (cat, the), (cat, sat), (sat, cat).</p>
<p>Predicting across a whole vocabulary would be slow, so <b>negative sampling</b> turns this into a yes/no question: score the real context word high, and a few random words low.</p>
<p style="text-align:center"><b>loss = −ln σ(c·p) − Σ ln σ(−c·n)</b></p>
<p>With centre c = (1, 0), true context p = (1, 0), and negatives (−1, 0) and (0, 1):</p>
<table><tr><th>Word</th><th>Dot with c</th><th>Term</th><th>Value</th></tr>
<tr><td>True context</td><td>1</td><td>−ln σ(1)</td><td>0.3133</td></tr>
<tr><td>Negative 1</td><td>−1</td><td>−ln σ(1)</td><td>0.3133</td></tr>
<tr><td>Negative 2</td><td>0</td><td>−ln σ(0)</td><td>0.6931</td></tr>
<tr><td colspan="3"><b>Total</b></td><td><b>1.3197</b></td></tr></table>
<p>Negative 2 costs most: it's at right angles, neither pushed away nor pulled. Training raises the dot with real neighbours and lowers it with random words.</p>
<p>This is an early, simple form of <b>contrastive learning</b>, and it's still the core idea in modern embedding models: pull related things together, push unrelated things apart.</p>
<p><b>Static vs contextual:</b> word2vec gives "bank" one vector, whether it's a river bank or a money bank. Transformer models produce a different vector for each occurrence, based on its surroundings. That's the main reason they replaced it.</p>
""", practice=["Skip-Gram Pairs", "Negative Sampling Loss"])


LESSON("Advanced", "Sentence embeddings and positions", """
<p><b>From tokens to one vector.</b> Search and RAG need one vector per text. The usual way is mean pooling (ignoring padding), then scaling to length 1:</p>
<ul><li>Tokens (3, 0), (0, 4), and a padding row (9, 9).</li><li>Mean of real tokens: (1.5, 2).</li><li>Length: √(1.5² + 2²) = 2.5.</li><li>Result: <b>(0.6, 0.8)</b>.</li></ul>
<p>After scaling, cosine similarity is just a dot product, which is why vector databases love it. If padding is left in, the result changes completely, and two identical texts in different batches get different vectors.</p>
<p><b>Giving order back.</b> Attention, in the next topic, treats its input as an unordered set, so position has to be added explicitly. The original transformer used fixed sine waves:</p>
<table><tr><th>Position</th><th>sin(pos)</th><th>cos(pos)</th><th>sin(pos/100)</th><th>cos(pos/100)</th></tr>
<tr><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td></tr>
<tr><td>1</td><td>0.8415</td><td>0.5403</td><td>0.01</td><td>1.0</td></tr>
<tr><td>2</td><td>0.9093</td><td>−0.4161</td><td>0.02</td><td>0.9998</td></tr></table>
<p>(These are n = 3, d = 4, where the rate for the second pair is 10000^(2/4) = 100.)</p>
<p>Think of a clock: the fast hand separates nearby positions, slow hands separate distant ones, and the chart shows these bands. Many models now use <b>learned position embeddings</b> or other schemes instead, but the purpose is the same.</p>
""", practice=["Sentence Embedding by Mean Pooling", "Sinusoidal Positional Encoding"])


@LD
def position_bands():
    n, d = 60, 32
    pos = np.arange(n)[:, None]
    rates = 10000 ** (np.arange(0, d, 2) / d)
    pe = np.zeros((n, d))
    pe[:, 0::2] = np.sin(pos / rates)
    pe[:, 1::2] = np.cos(pos / rates)
    fig, ax = plt.subplots(figsize=(4.8, 2.8))
    image = ax.imshow(pe, aspect="auto", cmap="RdBu")
    fig.colorbar(image, ax=ax)
    ax.set_xlabel("dimension")
    ax.set_ylabel("position")
