from sklearn.ensemble import GradientBoostingClassifier

class MLPruner:
    def __init__(self):
        self.model = GradientBoostingClassifier()
        self.trained = False

    def train(self, X, y):
        self.model.fit(X, y)
        self.trained = True

    def predict_proba(self, features):
        if not self.trained:
            return 1.0
        return self.model.predict_proba([features])[0][1]