import streamlit as st
import pandas as pd

# Mock model prediction function
def mock_predict(experience_level, tools, location, company_size):
    # Simple mock function to simulate model predictions
    return 100000 + (len(tools) * 5000)

# Streamlit app definition
def main():
    st.title('Data Scientist Salary Predictor')
    st.write("Predict your salary based on your experience level and other optional parameters.")

    # Input fields
    experience_level = st.selectbox('Level of Experience', ['Entry-level', 'Mid-level', 'Senior-level'])
    tools = st.multiselect('Tools', ['Python', 'SQL', 'R', 'TensorFlow', 'Keras', 'Scikit-learn'])
    location = st.selectbox('Location', ['USA', 'Canada', 'UK', 'Germany', 'India', 'Others'])
    company_size = st.selectbox('Company Size', ['Small', 'Medium', 'Large'])

    if st.button('Predict Salary'):
        # Use mock prediction function
        predicted_salary = mock_predict(experience_level, tools, location, company_size)
        st.markdown(
            f"<div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px; text-align: center; font-size: 24px; font-weight: bold;'>"
            f"Predicted Salary: ${predicted_salary:,.2f}"
            f"</div>",
            unsafe_allow_html=True
        )

if __name__ == '__main__':
    main()
