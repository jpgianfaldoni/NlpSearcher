from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_distances
import numpy as np

class SearchEngine:
    def __init__(self):
        pass

    def indexar(self, corpora, urls):
        self.vec = TfidfVectorizer()
        self.data = self.vec.fit_transform(corpora)
        self.info = [c[0:200] for c in corpora]
        self.urls = [u for u in urls]
        return

    def ranquear(self, string_de_busca, n_max=10):
        query = self.vec.transform([string_de_busca])
        print(query)
        dists = cosine_distances(query, self.data)
        idx = np.argsort(dists)
        webtexts = [ self.info[i] for i in idx[0,0:n_max]]
        weburls = [self.urls[i] for i in idx[0,0:n_max]]
        return webtexts, weburls