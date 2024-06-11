import streamlit as st
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

# Function to call the FastAPI prediction endpoint
def get_prediction(work_year, experience_level, employment_type, job_title, employee_residence, remote_ratio, company_size, company_location_grouped):
    url = "http://127.0.0.1:8000/predict"
    params = {
        "work_year": work_year,
        "experience_level": experience_level,
        "employment_type": employment_type,
        "job_title": job_title,
        "employee_residence": employee_residence,
        "remote_ratio": remote_ratio,
        "company_size": company_size,
        "company_location_grouped": company_location_grouped
    }
    logger = logging.getLogger()
    response = requests.get(url, params=params)
    logger.info(f"Response status code: {response.status_code}")
    logger.info(f"Response text: {response.text}")
    if response.status_code == 200:
        response_json = response.json()
        logger.info(f"Response JSON: {response_json}")
        if "prediction" in response_json:
            return float(response_json["prediction"])  # Ensure the prediction is converted to a float
        else:
            st.error(f"Error: {response_json}")
            return "Error: Could not get prediction"
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return "Error: Could not get prediction"

# Streamlit app definition
def main():
    st.title('Data Scientist Salary Predictor')
    st.write("Predict your salary based on your experience level and other optional parameters.")

    # Input fields
    experience_level_map = {'Entry-level': 1, 'Mid-level': 2, 'Senior-level': 3}
    employment_type_map = {'Full-time': 1, 'Part-time': 2, 'Contract': 3, 'Intern': 4}
    job_title_map = {'Engineering': 1, 'Data Science': 2, 'Analytics': 3, 'Machine Learning': 4, 'Others': 5}
    location_map = {'US': 'US', 'GB': 'GB', 'CA': 'CA', 'ES': 'ES', 'IN': 'IN', 'DE': 'DE', 'FR': 'FR',
                    'Rest of Asia': 'Rest_of_Asia', 'Mexico and Latin America': 'Latin_America', 'Rest of the world': 'Rest_of_the_World'}
    remote_ratio_map = {'0%': 0, '50%': 50, '100%': 100}
    company_size_map = {'Small': 1, 'Medium': 2, 'Large': 3}


    work_year = 2024  # Assuming work_year is always 2024
    experience_level = st.selectbox('Level of Experience', list(experience_level_map.keys()))
    employment_type = st.selectbox('Employment Type', list(employment_type_map.keys()))
    job_title = st.selectbox('Job Title', list(job_title_map.keys()))
    location = st.selectbox('Location', list(location_map.keys()))
    remote_ratio = st.selectbox('Remote Ratio', list(remote_ratio_map.keys()))


    st.write("If you are making a prediction for a known company, you can enter the following:")
    company_size = st.selectbox('Company Size (optional)', ['Select', 'Small', 'Medium', 'Large'])
    company_location = st.selectbox('Company Location (optional)', ['Select'] + list(location_map.keys()))

    # Use the same value as location if company_location is 'Select'
    if company_location == 'Select':
        company_location = location

    if company_size == 'Select':
        company_size = None
    else:
        company_size = company_size_map[company_size]

    if st.button('Predict Salary'):
       # Call the FastAPI endpoint for prediction
        predicted_salary = get_prediction(work_year, experience_level_map[experience_level], employment_type_map[employment_type],
                                          job_title_map[job_title], location_map[location], remote_ratio_map[remote_ratio],
                                          company_size, location_map[company_location])

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
