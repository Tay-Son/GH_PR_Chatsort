from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self, model_="sentence-transformers/all-distilroberta-v1"):
        self.model_ = model_
        self.embedder_ = SentenceTransformer()

    def run_(self):
