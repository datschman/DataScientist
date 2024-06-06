# package_folder/create_dummy_model.py
import os
import pickle
from models import DummyModel  # Import from models.py

# Ensure the directory exists
os.makedirs("package_folder/models", exist_ok=True)

class DummyModel:
    def predict(self, X):
        return [50000 for _ in X]

model = DummyModel()

with open("package_folder/models/dummy_model.pkl", "wb") as file:
    pickle.dump(model, file)
