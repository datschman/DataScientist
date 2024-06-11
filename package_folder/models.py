# package_folder/models.py
#class DummyModel:
#   def predict(self, X):
#        return [50000 for _ in X]




""" starting here: new code Stefan """
import os; print(os.getcwd())
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
import joblib
import pandas as pd
import numpy as np

# Print the current working directory for debugging
#print("Current working directory:", os.getcwd())


# Use absolute path to load the dataset
data_path = os.path.join(os.path.dirname(__file__), "../raw_data/ds_salaries.csv")
data = pd.read_csv(data_path)
print("Dataset loaded. Columns:", data.columns)

# Check the first few rows of the DataFrame
#print(data.head())

#define data
#data = pd.read_csv("../raw_data/ds_salaries.csv")
#data.head()

# Apply CLeaning Functions:
from cleaning import delete_duplicates, group_countries, group_job_titles
data = delete_duplicates(data)
data = group_countries(data)
data = group_job_titles(data)

#Define X and y (y needs to be log-transformed)
data["salary_in_usd_log"] = np.log(data['salary_in_usd'] + 0.0000001)
X = data.drop(columns=["salary", "salary_currency", "salary_in_usd", "salary_in_usd_log", "company_location", "job_title", "employment_type"])
y = data ["salary_in_usd_log"]

# Train, test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, shuffle=True, random_state=1)





# Model: Setup Pipeline for Encoding + Regression
###### Assign features to encoder-version
categorical_col = ["job_title_cluster", "company_location_grouped", "employee_residence"]
ordinal_col = ["work_year", "experience_level", "company_size"]

####### Define categories for ordinal_col
work_year_categories = ["2020", "2021", "2022", "2023", "2024"]
experience_level_categories = ["EN", "MI", "SE", "EX"]
employment_type_categories = ["PT", "FT", "CT", "FL"]
company_size_categories = ["S", "M", "L"]

####### Combine categories into final list
categories = [work_year_categories, experience_level_categories, company_size_categories]

####### Instantiate OrdinalEncoder with categories
ordinal_encoder = OrdinalEncoder(categories=categories)
categorial_encoder = OneHotEncoder(sparse_output = False, handle_unknown='ignore')

####### Create a pipeline for ordinal encoding and scaling
ordinal_pipeline = Pipeline([
    ('ordinal_encoder', ordinal_encoder),
    ('scaler', StandardScaler())
])

####### Parallelize the encoders
preprocessor = ColumnTransformer([
    ('ordinal_pipeline', ordinal_pipeline, ordinal_col),
    ('categorial_encoder', categorial_encoder, categorical_col)
])

# Create a  regressor
regressor = Ridge()

######## Create a model that includes the preprocessor and the regressor
model = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', regressor)
])

######## fit and transform your data with the model
model.fit(X_train, y_train)

# Predict and score the model
y_pred = model.predict(X_test)
model.score(X_test, y_test) # Score model
print(model.score(X_test, y_test))

# Construct the path to the model directory
model_dir = os.path.join(os.path.dirname(__file__), "models_pkl")

# Ensure the directory exists
os.makedirs(model_dir, exist_ok=True)

# Construct the path to the model file
model_path = os.path.join(model_dir, "real_model.pkl")

# Save the model
joblib.dump(model, model_path)
print(f"Model saved to {model_path}")
