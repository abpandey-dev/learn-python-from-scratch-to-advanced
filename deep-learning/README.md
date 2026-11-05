# Deep Learning & LLMs

10 topics · theory with 51 theory questions · 81 lessons from basics to advanced · 200 practice questions with answers · Tensors, training, CNNs, RNNs, embeddings, attention and transformers, language models, building LLM apps, RAG, agents and evaluation · everything is built from scratch so you can see inside it, then written the efficient way, both shown running step by step.

**Live site:** https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/

Every solution is run against its test cases by `build.py` before the site is generated, and each animation is recorded from a real run of the code you see.

## Topics

- [Tensors & Layers](#tensors-layers) — The language of deep learning: tensor shapes and batches, dense layers, logits, softmax and stable cross-entropy, initialisation, and backpropagation through real matrices.
- [Training Deep Networks](#training-deep-networks) — How to make deep networks learn: momentum, RMSProp, Adam and AdamW, learning-rate schedules and warm-up, batch and layer normalisation, gradient clipping, label smoothing, early stopping and gradient accumulation.
- [Convolutional Networks](#convolutional-networks) — How networks see: convolution by hand, stride and padding, output sizes, parameter counts, pooling, receptive fields, channels, 1×1 convolutions and residual connections.
- [RNNs & Sequences](#rnns-sequences) — Models with memory: the RNN cell, unrolling over time, vanishing gradients, LSTM and GRU cells by hand, padding and masks, teacher forcing and preparing sequence data.
- [Tokens & Embeddings](#tokens-embeddings) — How text becomes numbers: tokenising, BPE merges, bag of words and TF-IDF, embedding tables, skip-gram and negative sampling, word analogies, co-occurrence and positional encoding.
- [Attention & Transformers](#attention-transformers) — The idea behind every modern LLM: scaled dot-product attention by hand, masks, self- and cross-attention, multi-head attention, positional information and the full transformer block.
- [Language Models](#language-models) — How an LLM predicts and generates: bigram models by hand, perplexity, the shifted cross-entropy loss, temperature, top-k, top-p, beam search, repetition penalties and the KV cache.
- [Building With LLMs](#building-with-llms) — Writing real LLM applications: prompts and few-shot examples, tokens and costs, context budgets, structured output, retries, streaming, tool calling and caching, then calling the Claude API.
- [RAG & Retrieval](#rag-retrieval) — Answering from your own documents: chunking, TF-IDF and BM25, vector search, approximate indexes, fusion, MMR, re-ranking, citations and measuring retrieval with recall, MRR and nDCG.
- [Agents, Evals & Production](#agents-evals-production) — Taking LLMs to production: agent loops and their guard rails, evaluation metrics and comparing models fairly, latency, cost, rate limiting, safety checks, quantisation, fine-tuning and monitoring drift.

## Tensors & Layers

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Shape of a Nested List](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/tensors/shape-of-a-nested-list) | Easy | What a tensor is |
| 2 | [Flatten a Batch of Images](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/tensors/flatten-a-batch-of-images) | Easy | (n, h, w) → (n, h·w) |
| 3 | [Broadcast Result Shape](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/tensors/broadcast-result-shape) | Medium | Will these tensors combine? |
| 4 | [Dense Layer Forward](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/tensors/dense-layer-forward) | Easy | Z = X·W + b |
| 5 | [Two-Layer Forward Pass](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/tensors/two-layer-forward-pass) | Medium | Input → ReLU → output |
| 6 | [Model Memory](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/tensors/model-memory) | Easy | Parameters × bytes |
| 7 | [One-Hot a Batch of Labels](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/tensors/one-hot-a-batch-of-labels) | Easy | Targets for softmax |
| 8 | [Softmax for a Batch, Safely](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/tensors/softmax-for-a-batch-safely) | Medium | No overflow |
| 9 | [Cross-Entropy From Logits](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/tensors/cross-entropy-from-logits) | Medium | Log-sum-exp |
| 10 | [Binary Cross-Entropy From a Logit](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/tensors/binary-cross-entropy-from-a-logit) | Medium | The stable formula |
| 11 | [Mean Squared Error of a Batch](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/tensors/mean-squared-error-of-a-batch) | Easy | Averaged over all entries |
| 12 | [Accuracy From Logits](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/tensors/accuracy-from-logits) | Easy | Argmax |
| 13 | [Top-k Predictions](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/tensors/top-k-predictions) | Easy | Most likely classes |
| 14 | [Steps per Epoch](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/tensors/steps-per-epoch) | Easy | Batches and updates |
| 15 | [Shuffled Mini-Batches](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/tensors/shuffled-mini-batches) | Medium | A new order each epoch |
| 16 | [Gradient of a Linear Layer](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/tensors/gradient-of-a-linear-layer) | Medium | ∂MSE/∂W |
| 17 | [Backprop Through Two Layers](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/tensors/backprop-through-two-layers) | Hard | Matrix gradients |
| 18 | [Gradient Check](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/tensors/gradient-check) | Medium | Catching backprop bugs |
| 19 | [Initialisation Scales](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/tensors/initialisation-scales) | Easy | Glorot and He |
| 20 | [Variance Through a Layer](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/tensors/variance-through-a-layer) | Medium | Why scale matters |

## Training Deep Networks

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [SGD Update](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/training/sgd-update) | Easy | w ← w − η·g |
| 2 | [SGD With Momentum](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/training/sgd-with-momentum) | Medium | Velocity |
| 3 | [RMSProp Step Sizes](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/training/rmsprop-step-sizes) | Medium | Divide by recent gradient size |
| 4 | [Adam With Bias Correction](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/training/adam-with-bias-correction) | Hard | The default optimiser |
| 5 | [AdamW vs L2 Penalty](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/training/adamw-vs-l2-penalty) | Hard | Decoupled weight decay |
| 6 | [Step Decay Schedule](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/training/step-decay-schedule) | Easy | Drop every few epochs |
| 7 | [Cosine Schedule](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/training/cosine-schedule) | Easy | Smooth decay |
| 8 | [Warm-Up Then Cosine](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/training/warm-up-then-cosine) | Medium | The transformer schedule |
| 9 | [Clip Gradients by Norm](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/training/clip-gradients-by-norm) | Easy | Stops explosions |
| 10 | [Clip Gradients by Value](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/training/clip-gradients-by-value) | Easy | Keeps it simple, changes direction |
| 11 | [Batch Normalisation](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/training/batch-normalisation) | Medium | Per feature, across the batch |
| 12 | [Layer Normalisation](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/training/layer-normalisation) | Medium | Per row: used in transformers |
| 13 | [Running Statistics for Inference](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/training/running-statistics-for-inference) | Medium | Exponential moving average |
| 14 | [L2 Penalty in the Gradient](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/training/l2-penalty-in-the-gradient) | Easy | Weight decay |
| 15 | [Dropout During Training](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/training/dropout-during-training) | Medium | Keep, then rescale |
| 16 | [Label Smoothing](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/training/label-smoothing) | Easy | Don't aim for 100% |
| 17 | [Early Stopping](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/training/early-stopping) | Medium | Know when to stop |
| 18 | [Smoothing a Loss Curve](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/training/smoothing-a-loss-curve) | Easy | EMA with bias correction |
| 19 | [Gradient Accumulation](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/training/gradient-accumulation) | Medium | Big batch on a small GPU |
| 20 | [Pick a Learning Rate From a Range Test](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/training/pick-a-learning-rate-from-a-range-test) | Medium | Steepest fall |

## Convolutional Networks

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [1-D Convolution](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/cnn/1-d-convolution) | Easy | Slide and multiply |
| 2 | [1-D Convolution With Padding](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/cnn/1-d-convolution-with-padding) | Easy | Keep the edges |
| 3 | [Output Size](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/cnn/output-size) | Easy | ⌊(n + 2p − k)/s⌋ + 1 |
| 4 | [2-D Convolution](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/cnn/2-d-convolution) | Medium | A filter over an image |
| 5 | [Detect a Vertical Edge](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/cnn/detect-a-vertical-edge) | Easy | The Sobel filter |
| 6 | [Convolution With Stride](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/cnn/convolution-with-stride) | Medium | Skip positions |
| 7 | [Max Pooling](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/cnn/max-pooling) | Easy | Keep the strongest |
| 8 | [Average Pooling](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/cnn/average-pooling) | Easy | Smooth and shrink |
| 9 | [Global Average Pooling](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/cnn/global-average-pooling) | Easy | One number per channel |
| 10 | [Parameters in a Conv Layer](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/cnn/parameters-in-a-conv-layer) | Easy | (k·k·in + 1)·out |
| 11 | [Dense vs Conv Parameters](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/cnn/dense-vs-conv-parameters) | Easy | Why CNNs exist |
| 12 | [Operations in a Conv Layer](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/cnn/operations-in-a-conv-layer) | Medium | Parameters aren't cost |
| 13 | [Receptive Field](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/cnn/receptive-field) | Medium | How much each output sees |
| 14 | [Shape Through a Network](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/cnn/shape-through-a-network) | Medium | Track sizes before coding |
| 15 | [Flatten Size for the Classifier](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/cnn/flatten-size-for-the-classifier) | Easy | The number everyone gets wrong |
| 16 | [Convolution Across Channels](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/cnn/convolution-across-channels) | Hard | One filter sees all colours |
| 17 | [1×1 Convolution](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/cnn/1-1-convolution) | Medium | Mix channels, keep the size |
| 18 | [Normalise Image Channels](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/cnn/normalise-image-channels) | Easy | Mean and std per colour |
| 19 | [Flip Augmentation](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/cnn/flip-augmentation) | Easy | More data for free |
| 20 | [A Residual Block](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/cnn/a-residual-block) | Medium | Output = x + F(x) |

## RNNs & Sequences

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [One RNN Step](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rnn/one-rnn-step) | Easy | New memory from old memory |
| 2 | [Run an RNN Over a Sequence](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rnn/run-an-rnn-over-a-sequence) | Easy | Unrolling |
| 3 | [A Vector RNN Step](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rnn/a-vector-rnn-step) | Medium | With matrices |
| 4 | [Parameters: RNN, GRU, LSTM](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rnn/parameters-rnn-gru-lstm) | Easy | 3, then 4 gates' worth |
| 5 | [How Gradients Fade Through Time](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rnn/how-gradients-fade-through-time) | Easy | wᵗ |
| 6 | [Backprop Through Time](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rnn/backprop-through-time) | Hard | Chain over steps |
| 7 | [An LSTM Gate](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rnn/an-lstm-gate) | Easy | A soft on/off switch |
| 8 | [One LSTM Step](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rnn/one-lstm-step) | Hard | Forget, add, output |
| 9 | [Memory Across Many Steps](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rnn/memory-across-many-steps) | Medium | Why the cell state survives |
| 10 | [One GRU Step](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rnn/one-gru-step) | Hard | A simpler LSTM |
| 11 | [Pad a Batch of Sequences](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rnn/pad-a-batch-of-sequences) | Easy | Same length for a tensor |
| 12 | [Mask From Lengths](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rnn/mask-from-lengths) | Easy | 1 for real, 0 for padding |
| 13 | [Masked Average Loss](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rnn/masked-average-loss) | Medium | Ignore padding |
| 14 | [Last Real Output of Each Sequence](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rnn/last-real-output-of-each-sequence) | Medium | Not the padding |
| 15 | [Bidirectional States](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rnn/bidirectional-states) | Medium | Read both ways |
| 16 | [Sliding Windows for Forecasting](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rnn/sliding-windows-for-forecasting) | Easy | Turning a series into examples |
| 17 | [Teacher Forcing Targets](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rnn/teacher-forcing-targets) | Easy | Predict the next token |
| 18 | [Truncated BPTT Chunks](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rnn/truncated-bptt-chunks) | Medium | Long sequences in pieces |
| 19 | [Encode, Decode With a Vocabulary](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rnn/encode-decode-with-a-vocabulary) | Easy | Text ↔ numbers |
| 20 | [Average of the Real States](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rnn/average-of-the-real-states) | Medium | Mean pooling over time |

## Tokens & Embeddings

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Word Tokeniser](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/embeddings/word-tokeniser) | Easy | Splitting text |
| 2 | [Build a Vocabulary](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/embeddings/build-a-vocabulary) | Easy | With special tokens |
| 3 | [Encode With Unknowns](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/embeddings/encode-with-unknowns) | Easy | Unseen words |
| 4 | [Bag of Words](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/embeddings/bag-of-words) | Easy | Counts per document |
| 5 | [TF-IDF](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/embeddings/tf-idf) | Medium | Rare words count more |
| 6 | [BPE: Most Frequent Pair](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/embeddings/bpe-most-frequent-pair) | Medium | How tokenisers are built |
| 7 | [BPE: Apply a Merge](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/embeddings/bpe-apply-a-merge) | Medium | Joining a pair |
| 8 | [BPE: Train n Merges](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/embeddings/bpe-train-n-merges) | Hard | A tiny tokeniser |
| 9 | [Rough Token Estimate](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/embeddings/rough-token-estimate) | Easy | Before you call an API |
| 10 | [Embedding Lookup](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/embeddings/embedding-lookup) | Easy | A table of vectors |
| 11 | [Embedding Table Size](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/embeddings/embedding-table-size) | Easy | It adds up |
| 12 | [Most Similar Vectors](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/embeddings/most-similar-vectors) | Medium | Cosine search |
| 13 | [Word Analogy](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/embeddings/word-analogy) | Medium | king − man + woman |
| 14 | [Skip-Gram Pairs](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/embeddings/skip-gram-pairs) | Easy | Word2vec's training data |
| 15 | [Co-occurrence Matrix](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/embeddings/co-occurrence-matrix) | Medium | Words known by their neighbours |
| 16 | [Pointwise Mutual Information](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/embeddings/pointwise-mutual-information) | Medium | More than chance? |
| 17 | [Negative Sampling Loss](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/embeddings/negative-sampling-loss) | Hard | Pull together, push apart |
| 18 | [Sentence Embedding by Mean Pooling](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/embeddings/sentence-embedding-by-mean-pooling) | Medium | Ignore padding |
| 19 | [Sinusoidal Positional Encoding](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/embeddings/sinusoidal-positional-encoding) | Medium | Giving order to a set |
| 20 | [Truncate and Pad to a Fixed Length](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/embeddings/truncate-and-pad-to-a-fixed-length) | Easy | Every model has a limit |

## Attention & Transformers

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Attention Scores](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/attention/attention-scores) | Easy | Query × key ÷ √d |
| 2 | [Attention Weights](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/attention/attention-weights) | Easy | Softmax per query |
| 3 | [Scaled Dot-Product Attention](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/attention/scaled-dot-product-attention) | Medium | The core formula |
| 4 | [Soft Dictionary Lookup](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/attention/soft-dictionary-lookup) | Easy | The intuition in one dimension |
| 5 | [Causal Mask](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/attention/causal-mask) | Easy | Can't look ahead |
| 6 | [Masked Softmax](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/attention/masked-softmax) | Medium | Hidden positions get zero |
| 7 | [Padding Plus Causal Mask](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/attention/padding-plus-causal-mask) | Medium | Both rules together |
| 8 | [Masked Self-Attention](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/attention/masked-self-attention) | Hard | What a decoder does |
| 9 | [Self-Attention With Learned Projections](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/attention/self-attention-with-learned-projections) | Medium | Q, K and V from X |
| 10 | [Split Into Heads](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/attention/split-into-heads) | Medium | (T, d) → (h, T, d/h) |
| 11 | [Merge Heads](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/attention/merge-heads) | Easy | Back together |
| 12 | [Multi-Head Parameters](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/attention/multi-head-parameters) | Medium | Cost of attention |
| 13 | [Transformer Block Parameters](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/attention/transformer-block-parameters) | Medium | Where the size goes |
| 14 | [Position-Wise Feed-Forward](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/attention/position-wise-feed-forward) | Medium | The same small network at every position |
| 15 | [Add and Norm](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/attention/add-and-norm) | Medium | Residual + layer norm |
| 16 | [Cross-Attention](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/attention/cross-attention) | Medium | Decoder asks, encoder answers |
| 17 | [Add Positions to Embeddings](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/attention/add-positions-to-embeddings) | Easy | Learned positions |
| 18 | [Which Token Was Attended?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/attention/which-token-was-attended) | Easy | Reading the weights |
| 19 | [Attention Cost vs Length](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/attention/attention-cost-vs-length) | Easy | Why long inputs are expensive |
| 20 | [Weight Tying Savings](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/attention/weight-tying-savings) | Easy | Input and output share a table |

## Language Models

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Bigram Counts](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/language-models/bigram-counts) | Easy | What follows what |
| 2 | [Bigram Probability With Smoothing](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/language-models/bigram-probability-with-smoothing) | Easy | Unseen pairs aren't impossible |
| 3 | [Log-Probability of a Sentence](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/language-models/log-probability-of-a-sentence) | Medium | Add logs, don't multiply |
| 4 | [Perplexity](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/language-models/perplexity) | Easy | The effective number of choices |
| 5 | [Next-Token Cross-Entropy](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/language-models/next-token-cross-entropy) | Medium | The loss of every LLM |
| 6 | [Ignore Padding in the Loss](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/language-models/ignore-padding-in-the-loss) | Medium | ignore_index = −100 |
| 7 | [Make a Training Batch](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/language-models/make-a-training-batch) | Easy | Random windows from a long text |
| 8 | [One Learning Step on Logits](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/language-models/one-learning-step-on-logits) | Medium | Neural bigram |
| 9 | [Backoff When a Pair Is Unseen](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/language-models/backoff-when-a-pair-is-unseen) | Medium | Fall back on the single word |
| 10 | [Temperature](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/language-models/temperature) | Easy | Cautious or adventurous |
| 11 | [Top-k Filtering](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/language-models/top-k-filtering) | Easy | Keep the best k |
| 12 | [Top-p (Nucleus) Filtering](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/language-models/top-p-nucleus-filtering) | Medium | Keep enough to reach p |
| 13 | [Sampling With a Random Number](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/language-models/sampling-with-a-random-number) | Easy | How a choice is actually made |
| 14 | [Greedy Generation](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/language-models/greedy-generation) | Medium | Always the top choice |
| 15 | [Beam Search](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/language-models/beam-search) | Hard | Keep several candidates |
| 16 | [Repetition Penalty](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/language-models/repetition-penalty) | Medium | Stop saying the same thing |
| 17 | [Stop Sequences](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/language-models/stop-sequences) | Easy | Know when to finish |
| 18 | [Context Window](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/language-models/context-window) | Easy | The model only sees so much |
| 19 | [What the KV Cache Saves](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/language-models/what-the-kv-cache-saves) | Medium | Don't recompute the past |
| 20 | [How Unsure Is the Model?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/language-models/how-unsure-is-the-model) | Easy | Entropy of the next token |

## Building With LLMs

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Fill a Prompt Template](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/llm-apps/fill-a-prompt-template) | Easy | Reusable prompts |
| 2 | [Few-Shot Prompt](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/llm-apps/few-shot-prompt) | Easy | Teach by example |
| 3 | [Wrap Untrusted Text](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/llm-apps/wrap-untrusted-text) | Medium | Separate data from instructions |
| 4 | [Merge Consecutive Roles](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/llm-apps/merge-consecutive-roles) | Medium | User and assistant alternate |
| 5 | [Estimate a Request's Cost](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/llm-apps/estimate-a-requests-cost) | Easy | Know before you scale |
| 6 | [Fit History Into a Budget](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/llm-apps/fit-history-into-a-budget) | Medium | Keep the newest turns |
| 7 | [Room Left for the Answer](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/llm-apps/room-left-for-the-answer) | Easy | Input and output share the window |
| 8 | [Pull JSON Out of a Reply](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/llm-apps/pull-json-out-of-a-reply) | Medium | Models add chatter |
| 9 | [Validate Model Output](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/llm-apps/validate-model-output) | Medium | Never trust the shape |
| 10 | [Match a Reply to a Label](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/llm-apps/match-a-reply-to-a-label) | Easy | Classification output |
| 11 | [Backoff Delays](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/llm-apps/backoff-delays) | Easy | Wait longer each time |
| 12 | [Retry the Right Errors](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/llm-apps/retry-the-right-errors) | Medium | 429 yes, 400 no |
| 13 | [Assemble a Stream](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/llm-apps/assemble-a-stream) | Medium | Text arrives in pieces |
| 14 | [Run the Tool Calls](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/llm-apps/run-the-tool-calls) | Medium | The model asks; your code acts |
| 15 | [The Tool Loop With a Fake Model](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/llm-apps/the-tool-loop-with-a-fake-model) | Hard | An agent in miniature |
| 16 | [Handle Every Stop Reason](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/llm-apps/handle-every-stop-reason) | Easy | Don't assume it finished |
| 17 | [Response Cache by Hash](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/llm-apps/response-cache-by-hash) | Medium | Same request, same answer |
| 18 | [Prompt Cache Prefix](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/llm-apps/prompt-cache-prefix) | Medium | Only the start is reusable |
| 19 | [Batch Under Two Limits](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/llm-apps/batch-under-two-limits) | Medium | Count and tokens |
| 20 | [How Long Will a Batch Take?](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/llm-apps/how-long-will-a-batch-take) | Easy | Rate limits |

## RAG & Retrieval

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Fixed-Size Chunks](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rag/fixed-size-chunks) | Easy | The simplest splitter |
| 2 | [Chunks With Overlap](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rag/chunks-with-overlap) | Easy | Don't cut facts in half |
| 3 | [Sentence-Aware Chunks](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rag/sentence-aware-chunks) | Medium | Keep sentences whole |
| 4 | [Rank by TF-IDF](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rag/rank-by-tf-idf) | Medium | Keyword search |
| 5 | [BM25 Score](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rag/bm25-score) | Hard | The standard for keyword search |
| 6 | [Vector Top-k](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rag/vector-top-k) | Easy | Semantic search |
| 7 | [Filter, Then Search](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rag/filter-then-search) | Medium | Metadata matters |
| 8 | [An Approximate Index](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rag/an-approximate-index) | Hard | Search only part of the data |
| 9 | [Reciprocal Rank Fusion](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rag/reciprocal-rank-fusion) | Medium | Combine two rankings |
| 10 | [Maximal Marginal Relevance](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rag/maximal-marginal-relevance) | Hard | Relevant but not repetitive |
| 11 | [Re-Rank the Candidates](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rag/re-rank-the-candidates) | Easy | Cheap first, careful second |
| 12 | [Say When You Don't Know](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rag/say-when-you-dont-know) | Easy | A retrieval threshold |
| 13 | [Remove Near-Duplicates](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rag/remove-near-duplicates) | Medium | Don't pay for repeats |
| 14 | [Fit Chunks Into the Budget](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rag/fit-chunks-into-the-budget) | Easy | Best first, until full |
| 15 | [Build the Prompt With Sources](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rag/build-the-prompt-with-sources) | Easy | Make answers checkable |
| 16 | [Check the Citations](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rag/check-the-citations) | Medium | Catch invented sources |
| 17 | [Recall@k](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rag/recall-k) | Easy | Did we find it? |
| 18 | [Precision@k](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rag/precision-k) | Easy | How much is noise? |
| 19 | [Mean Reciprocal Rank](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rag/mean-reciprocal-rank) | Medium | How high is the first hit? |
| 20 | [nDCG@k](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/rag/ndcg-k) | Hard | Graded relevance, order matters |

## Agents, Evals & Production

| # | Question | Level | Concept |
|---|---|---|---|
| 1 | [Agent Loop With a Step Limit](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/agents-production/agent-loop-with-a-step-limit) | Medium | Always bound the loop |
| 2 | [Validate Tool Input](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/agents-production/validate-tool-input) | Medium | Check before you run |
| 3 | [Spot a Stuck Agent](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/agents-production/spot-a-stuck-agent) | Medium | The same call again and again |
| 4 | [Permission Gate](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/agents-production/permission-gate) | Easy | Risky actions need a person |
| 5 | [Normalised Exact Match](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/agents-production/normalised-exact-match) | Easy | The simplest metric |
| 6 | [Token F1](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/agents-production/token-f1) | Medium | Partial credit |
| 7 | [Clipped Word Precision](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/agents-production/clipped-word-precision) | Medium | The core of BLEU |
| 8 | [Compare Two Models Fairly](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/agents-production/compare-two-models-fairly) | Easy | Same examples, side by side |
| 9 | [Bootstrap the Difference](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/agents-production/bootstrap-the-difference) | Medium | Is the gap real? |
| 10 | [Regression Gate](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/agents-production/regression-gate) | Easy | Stop a bad release |
| 11 | [Latency Percentiles](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/agents-production/latency-percentiles) | Easy | The mean hides the pain |
| 12 | [What Caching Saves](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/agents-production/what-caching-saves) | Medium | Run the numbers |
| 13 | [Token Bucket Rate Limiter](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/agents-production/token-bucket-rate-limiter) | Medium | Allow bursts, cap the average |
| 14 | [Choose a Model by Need](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/agents-production/choose-a-model-by-need) | Easy | Cheapest that does the job |
| 15 | [Injection Phrase Check](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/agents-production/injection-phrase-check) | Easy | Useful, but easy to beat |
| 16 | [Redact Personal Data](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/agents-production/redact-personal-data) | Medium | Before you log it |
| 17 | [Memory at Each Precision](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/agents-production/memory-at-each-precision) | Easy | Why quantisation matters |
| 18 | [Quantise to 8 Bits](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/agents-production/quantise-to-8-bits) | Medium | Fewer bits, small errors |
| 19 | [LoRA Parameters](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/agents-production/lora-parameters) | Easy | Fine-tune a tiny slice |
| 20 | [Population Stability Index](https://abpandey-dev.github.io/learn-python-from-scratch-to-advanced/deep-learning/#/q/agents-production/population-stability-index) | Medium | Has the input drifted? |

## Build

```bash
python3 handbook/build.py --book deep-learning
```

Sources live in `deep-learning/src/`: `topics/` (questions and solutions), `lessons/` and `theory/`.
