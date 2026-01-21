import hashlib
import numpy as np

class Embedder:
    """
    Lightweight deterministic embedder (no torch).
    Converts text into a fixed-size vector using hashing.
    """

    def __init__(self, dim: int = 384):
        self.dim = dim

    def _hash_to_index(self, token: str) -> int:
        h = hashlib.md5(token.encode("utf-8")).hexdigest()
        return int(h, 16) % self.dim

    def encode(self, texts):
        vectors = []
        for text in texts:
            vec = np.zeros(self.dim, dtype=np.float32)
            tokens = str(text).lower().split()

            for t in tokens:
                idx = self._hash_to_index(t)
                vec[idx] += 1.0

            # normalize
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm

            vectors.append(vec.tolist())
        return vectors
