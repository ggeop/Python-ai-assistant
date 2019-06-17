from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity, euclidean_distances

from jarvis.skills.skills_registry import BASIC_SKILLS


class Analyzer:
    def __init__(self, weight_measure, similarity_measure, args):
        self.weight_measure = weight_measure
        self.similarity_measure = similarity_measure
        self.args = args
        self.vectorizer = self.create_vectorizer()

    @property
    def tags(self):
        tags_list = []
        for skill in BASIC_SKILLS.values():
            tags_list.append(list(skill['tags']))
        return [' '.join(tag) for tag in tags_list]


    def create_vectorizer(self):
        return self.weight_measure(**self.args)

    # Create/train the model
    def _train_model(self):
        return self.vectorizer.fit_transform(self.tags)

    def _score(self, user_transcript):

        train_tdm = self._train_model()
        test_tdm = self.vectorizer.transform([user_transcript])

        # Calculate similarities
        similarities = self.similarity_measure(train_tdm, test_tdm)

        # Extract the most similar skill
        indexes = similarities.argsort(axis=None)
        index_score = [(index, similarities[index]) for index in indexes]

        return index_score

    def extract(self, user_transcript):
        skills = [index for index, score in self._score(user_transcript) if score > 0]
        return skills


user_transcript = 'date'

# Model arguments
# To make TfidfVectorizer behave as CountVectorize "norm": None and "use_idf": False
args = {

    "stop_words": "english",
    "lowercase": True,
    "norm": 'l1',
    "use_idf": True,
}


searcher = Analyzer(weight_measure=TfidfVectorizer,
                    similarity_measure=linear_kernel,
                    args=args)

skill = searcher.extract(user_transcript)
