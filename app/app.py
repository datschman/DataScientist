import streamlit as st
import requests

# Function to call the FastAPI prediction endpoint
def get_prediction(experience_level, country):
    url = "http://127.0.0.1:8000/predict"
    params = {
        "experience_level": experience_level,
        "country": country
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return float(response.json()["prediction"])  # Ensure the prediction is converted to a float
    else:
        return "Error: Could not get prediction"

# Streamlit app definition
def main():
    st.title('Data Scientist Salary Predictor')
    st.write("Predict your salary based on your experience level and other optional parameters.")

    # Input fields
    experience_level_map = {'Entry-level': 1, 'Mid-level': 2, 'Senior-level': 3}
    country_map = {'USA': 1, 'Canada': 2, 'UK': 3, 'Germany': 4, 'India': 5, 'Others': 6}

    experience_level = st.selectbox('Level of Experience', list(experience_level_map.keys()))
    tools = st.multiselect('Tools', ['Python', 'SQL', 'R', 'TensorFlow', 'Keras', 'Scikit-learn'])
    location = st.selectbox('Location', list(country_map.keys()))
    company_size = st.selectbox('Company Size', ['Small', 'Medium', 'Large'])

    if st.button('Predict Salary'):
        # Call the FastAPI endpoint for prediction
        predicted_salary = get_prediction(experience_level_map[experience_level], country_map[location])

        if isinstance(predicted_salary, str) and "Error" in predicted_salary:
            st.error(predicted_salary)
        else:
            st.markdown(
                f"<div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px; text-align: center; font-size: 24px; font-weight: bold;'>"
                f"Predicted Salary: ${predicted_salary:,.2f}"
                f"</div>",
                unsafe_allow_html=True
            )

if __name__ == '__main__':
    main()
