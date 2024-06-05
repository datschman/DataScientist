# package_folder/models.py
class DummyModel:
    def predict(self, X):
        return [50000 for _ in X]
