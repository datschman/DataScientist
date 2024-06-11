# Ensure the directory exists
#os.makedirs("package_folder/models", exist_ok=True)

#class DummyModel:
#def predict(self, X):
#        return [50000 for _ in X]

#model = DummyModel()

#with open("package_folder/models/dummy_model.pkl", "wb") as file:
    #pickle.dump(model, file)


# package_folder/create_dummy_model.py
import os
import joblib
from models import model  # Import the real model from models.py

# Print the current working directory for debugging
print("Current working directory:", os.getcwd())

# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the model directory
model_dir = os.path.join(current_dir, "models_pkl")

# Ensure the directory exists
os.makedirs(model_dir, exist_ok=True)

# Construct the path to the model file
model_path = os.path.join(model_dir, "real_model.pkl")

# Save the real model
with open(model_path, "wb") as file:
    joblib.dump(model, file)

print(f"Model saved to {model_path}")
