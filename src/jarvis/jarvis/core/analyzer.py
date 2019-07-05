class Analyzer:
    def __init__(self, weight_measure, similarity_measure, args, skills_):
        self.weight_measure = weight_measure
        self.similarity_measure = similarity_measure
        self.args = args
        self.skills = skills_

    @property
    def tags(self):
        tags_list = []
        for skill in self.skills.values():
            tags_list.append(list(skill['tags']))
        return [' '.join(tag) for tag in tags_list]

    @property
    def vectorizer(self):
        return self.weight_measure(**self.args)

    @property
    def train_tdm(self):
        return self.vectorizer.fit_transform(self.tags)

    def extract(self, user_transcript):
        test_tdm = self.vectorizer.transform([user_transcript])
        # Calculate similarities
        similarities = self.similarity_measure(self.train_tdm, test_tdm)
        # Extract the most similar skill
        skill_index = similarities.argsort(axis=None)[-1]
        if similarities[skill_index] > 0:
            skill_key = [skill for skill in enumerate(self.skills) if skill[0] == skill_index][0][1]
            return self.skills[skill_key]