"""
ClickBait Shield AI — Custom Model Classes
Definitions for 1D CNN and K-Means Classifier architectures.
"""
import re
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import MiniBatchKMeans

def clean_tokenize(text: str):
    """Splits into lower-case clean words."""
    return [re.sub(r'^[^\w]+|[^\w]+$', '', w).lower() for w in text.split() if w]

class Conv1DModel:
    """1D Convolutional Neural Network with spatial sequence convolution and max-pooling."""
    def __init__(self, vocab=None, embedding_dim=32, num_filters=48, max_len=20):
        self.vocab = vocab or {}
        self.embedding_dim = embedding_dim
        self.num_filters = num_filters
        self.max_len = max_len
        self.E = None
        self.W_conv = None
        self.b_conv = None
        self.dense = LogisticRegression(max_iter=500, random_state=42)

    def text_to_seq(self, texts):
        sequences = np.zeros((len(texts), self.max_len), dtype=np.int32)
        for i, text in enumerate(texts):
            tokens = clean_tokenize(text)
            for j, token in enumerate(tokens[:self.max_len]):
                sequences[i, j] = self.vocab.get(token, 1)
        return sequences

    def fit(self, texts, labels):
        V = len(self.vocab)
        self.E = np.random.randn(V, self.embedding_dim).astype(np.float32) * 0.1
        
        # Word-label frequency prior for embedding dim 0
        cb_counts = {}
        for text, lbl in zip(texts, labels):
            for w in clean_tokenize(text):
                if w in self.vocab:
                    idx = self.vocab[w]
                    cb_counts[idx] = cb_counts.get(idx, [0, 0])
                    cb_counts[idx][lbl] += 1

        for idx, (n0, n1) in cb_counts.items():
            total = n0 + n1
            if total >= 3:
                p_cb = (n1 + 1) / (total + 2)
                self.E[idx, 0] = (p_cb - 0.5) * 3.0

        np.random.seed(42)
        self.W_conv = np.random.randn(2 * self.embedding_dim, self.num_filters).astype(np.float32) * 0.1
        self.b_conv = np.zeros(self.num_filters, dtype=np.float32)

        X_seq = self.text_to_seq(texts)
        features = self._extract_features(X_seq)
        self.dense.fit(features, labels)

    def _extract_features(self, X_seq):
        emb = self.E[X_seq]  # (N, L, D)
        bigrams = np.concatenate([emb[:, :-1, :], emb[:, 1:, :]], axis=2)  # (N, L-1, 2D)
        conv = np.maximum(0, np.tensordot(bigrams, self.W_conv, axes=([2], [0])) + self.b_conv)  # (N, L-1, num_filters)
        pooled = np.max(conv, axis=1)  # (N, num_filters)
        return pooled

    def predict_proba(self, texts):
        X_seq = self.text_to_seq(texts)
        features = self._extract_features(X_seq)
        return self.dense.predict_proba(features)

    def predict(self, texts):
        probs = self.predict_proba(texts)[:, 1]
        return (probs >= 0.5).astype(int)


class KMeansClassifier:
    """K-Means Prototype Cluster Classifier."""
    def __init__(self, n_clusters=2, random_state=42):
        self.km = MiniBatchKMeans(n_clusters=n_clusters, random_state=random_state, batch_size=2048)
        self.cb_idx = 0
        self.legit_idx = 1
        self.c_cb = None
        self.c_legit = None

    def fit(self, X_tr, y_train):
        self.km.fit(X_tr)
        tr_clusters = self.km.predict(X_tr)
        c0_cb = np.mean([y_train[i] for i in range(len(y_train)) if tr_clusters[i] == 0])
        c1_cb = np.mean([y_train[i] for i in range(len(y_train)) if tr_clusters[i] == 1])
        self.cb_idx = 1 if c1_cb > c0_cb else 0
        self.legit_idx = 1 - self.cb_idx

        # Normalize centroid vectors for cosine similarity
        c_cb = self.km.cluster_centers_[self.cb_idx]
        c_legit = self.km.cluster_centers_[self.legit_idx]
        self.c_cb = c_cb / max(1e-6, np.linalg.norm(c_cb))
        self.c_legit = c_legit / max(1e-6, np.linalg.norm(c_legit))

    def predict_proba(self, X):
        sim_cb = X.dot(self.c_cb)
        sim_legit = X.dot(self.c_legit)
        diff = (sim_cb - sim_legit) * 20.0
        prob_cb = 1.0 / (1.0 + np.exp(-np.clip(diff, -15, 15)))
        return np.column_stack([1.0 - prob_cb, prob_cb])

    def predict(self, X):
        return (self.predict_proba(X)[:, 1] >= 0.5).astype(int)
