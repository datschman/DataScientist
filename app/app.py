import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests
import logging
import os
from PIL import Image

# Print the current working directory for debugging purposes
print(os.getcwd())

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

# Replace the FastAPI URL with the actual URL from Cloud Run
FASTAPI_URL = "https://fastapi-app-6jfxomnrna-uc.a.run.app"

# Function to call the FastAPI prediction endpoint
def get_prediction(work_year, experience_level, employment_type, job_title_cluster, remote_ratio, company_size, company_location_grouped):
    url = f"{FASTAPI_URL}/predict"
    params = {
        "work_year": work_year,
        "experience_level": experience_level,
        "employment_type": employment_type,
        "job_title_cluster": job_title_cluster,
        "remote_ratio": remote_ratio,
        "company_size": company_size,
        "company_location_grouped": company_location_grouped
    }
    logger.info(f"Request params: {params}")
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

# Function to group job titles
def group_job_titles(job_title):
    if 'data scientist' in job_title.lower():
        return 'Data Science'
    elif 'machine learning' in job_title.lower():
        return 'Machine Learning'
    elif 'analyst' in job_title.lower():
        return 'Analytics'
    elif 'engineer' in job_title.lower():
        return 'Engineering'
    else:
        return 'Other Data jobs'

# Function to generate and display salary distribution graphs
def display_salary_distribution(data):
    # Define custom salary ranges (bins) and labels
    bins = [0, 50000, 80000, 110000, 150000, float('inf')]
    labels = ['0-50k', '50-80k', '80-110k', '110-150k', '150k+']

    # Bin the salary data into the defined ranges
    data['salary_range'] = pd.cut(data['salary'], bins=bins, labels=labels, right=False)

    # Count the occurrences of each salary range
    salary_range_counts = data['salary_range'].value_counts().sort_index()

    # Plotting the number of occurrences of each salary range using a bar plot
    plt.figure(figsize=(7, 5))
    sns.barplot(x=salary_range_counts.index, y=salary_range_counts.values, palette=sns.light_palette("red", n_colors=5))
    plt.title('Salary Distribution for your Experience', fontsize=16, color='#333333')
    plt.xlabel('Salary Range', fontsize=12, color='#333333')
    plt.ylabel('Number of Occurrences', fontsize=12, color='#333333')
    plt.xticks(rotation=45, color='#333333')
    plt.yticks(color='#333333')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(plt)

# Function to generate and display proportion of occurrences for each experience level by the selected job category
def display_experience_level_by_job(data, selected_job_category):
    filtered_data = data[data['job_title_cluster'] == selected_job_category]
    plt.figure(figsize=(7, 5))
    sns.countplot(data=filtered_data, x='experience_level', order=['EN', 'MI', 'SE', 'EX'], palette=sns.color_palette("light:r", n_colors=4))
    plt.title('Job offers by Experience for your job Category', fontsize=16, color='#333333')
    plt.xlabel('Experience Level', fontsize=12, color='#333333')
    plt.ylabel('Count', fontsize=12, color='#333333')
    plt.xticks(rotation=45, color='#333333')
    plt.yticks(color='#333333')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(plt)

# Function to generate and display the impact of experience level on salaries styled like the provided example
def display_experience_level_impact_on_salaries(data):
    # Remove the top outlier in the second column
    mid_level_data = data[data['experience_level'] == 'MI']
    if not mid_level_data.empty:
        max_value = mid_level_data['salary_in_usd'].max()
        data = data[~((data['experience_level'] == 'MI') & (data['salary_in_usd'] == max_value))]

    plt.figure(figsize=(7, 5))
    sns.boxplot(data=data, x='experience_level', y='salary_in_usd', order=['EN', 'MI', 'SE', 'EX'], palette=sns.light_palette("red", n_colors=4))
    plt.title('Salary Overview by Experience', fontsize=16, color='#333333')
    plt.xlabel('Experience Level', fontsize=12, color='#333333')
    plt.ylabel('Salary (USD)', fontsize=12, color='#333333')
    plt.xticks(color='#333333')
    plt.yticks(color='#333333')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(plt)

# Streamlit app definition
def main():
    st.set_page_config(
        page_title="Data Science Career Navigator",
        page_icon="🧢",
        layout="wide"
    )

    # Custom CSS to adjust the layout and styles
    st.markdown(
        """
        <style>
        .header-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
        }
        .header-container img {
            width: 600px;  /* 8 times bigger */
            margin-right: 20px;  /* Space between image and text */
        }
        .header-text {
            flex: 1;
            text-align: center;
        }
        .header-text h1 {
            margin-bottom: 0;
        }
        .stButton button {
            background-color: lightcoral;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            cursor: pointer;
        }
        .stButton button:hover {
            background-color: #ff7f7f;
        }
        .salary-prediction {
            background-color: lightcoral;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: white;
        }
        .stApp {
            padding: 0;
        }
        .input-container {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-right: 20px;
        }
        .graph-container {
            flex: 1;
            padding-left: 20px;
        }
        .form-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .graph-description {
            margin-top: -20px;
            margin-bottom: 20px;
            font-size: 16px;
            color: #333333;
        }
        .footer {
            margin-top: 50px;
            text-align: center;
            font-size: 16px;
            color: #333333;
        }
        .footer img {
            width: 100px;  /* Adjust size as needed */
            margin-top: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1, 3])

    with col1:
        with st.form(key='salary_form'):
            st.write("## Start with your info:")
            experience_level_map = {'Entry-level': 'EN', 'Mid-level': 'MI', 'Senior-level': 'SE', 'Executive': 'EX'}
            employment_type_map = {'Full-time': 'FT', 'Part-time': 'PT', 'Contract': 'CT', 'Freelance': 'FL'}
            job_title_map = {'Data Science': 'Data Science', 'Machine Learning': 'Machine Learning', 'Analytics': 'Analytics', 'Engineering': 'Engineering', 'Other Data job': 'Other Data jobs'}
            location_map = {'US': 'US', 'GB': 'GB', 'CA': 'CA', 'ES': 'ES', 'IN': 'IN', 'DE': 'DE', 'FR': 'FR',
                            'Rest of Asia': 'Rest_of_Asia', 'Mexico and Latin America': 'Latin_America', 'Rest of the world': 'Rest_of_the_World', 'Rest of Europe': 'Rest_of_Europe'}
            remote_ratio_map = {'0%': 0, '50%': 50, '100%': 100}
            company_size_map = {'Small': 'S', 'Medium': 'M', 'Large': 'L'}

            work_year = 2024  # Assuming work_year is always 2024
            experience_level = st.selectbox('Level of Experience', list(experience_level_map.keys()))
            employment_type = st.selectbox('Employment Type', list(employment_type_map.keys()))
            job_title_cluster = st.selectbox('Job Title', list(job_title_map.keys()))
            remote_ratio = st.selectbox('Remote Ratio', list(remote_ratio_map.keys()))

            st.write("If you are making a prediction for a known company, you can enter the following:")
            company_size = st.selectbox('Company Size (optional)', ['Select', 'Small', 'Medium', 'Large'])
            company_location_grouped = st.selectbox('Company Location (optional)', ['Select'] + list(location_map.keys()))

            if company_location_grouped == 'Select':
                company_location_grouped = 'US'

            if company_size == 'Select':
                company_size = None
            else:
                company_size = company_size_map[company_size]

            form_submitted = st.form_submit_button(label='Predict Salary')

    with col2:
        left_co, cent_co,last_co = st.columns(3)
        with cent_co:
            st.image("DaTaSciencelogo.png", width=300)

        st.write("""
            Are you intrigued by the world of Data Science? We have something just for you! Simply input your personal details on the left, and voila! You’ll receive a personalized salary prediction tailored to your profile.
            Our Career Navigator employs a prediction model, built on data extracted from data job platforms. Use it as a compass in the exciting journey of Data Science! Remember, it’s not magic, it’s science!
        """)

        # Load your dataset
        data_path = os.path.join(os.path.dirname(__file__), "../raw_data/ds_salaries.csv")
        data = pd.read_csv(data_path)

        # Add job_title_cluster column using the group_job_titles function
        data['job_title_cluster'] = data['job_title'].apply(group_job_titles)

        # Display graphs
        col2_1, col2_2, col2_3 = st.columns(3)

        with col2_1:
            entry_level_data = data[data['experience_level'] == 'EN']
            display_salary_distribution(entry_level_data)

        with col2_2:
            display_experience_level_by_job(data, job_title_cluster)

        with col2_3:
            display_experience_level_impact_on_salaries(data)

        if form_submitted:
            predicted_salary = get_prediction(work_year, experience_level_map[experience_level], employment_type_map[employment_type],
                                              job_title_cluster, remote_ratio_map[remote_ratio],
                                              company_size, location_map[company_location_grouped])

            st.markdown("---")  # Adding a horizontal line to separate the graphs

            if isinstance(predicted_salary, str) and "Error" in predicted_salary:
                st.error(predicted_salary)
            else:
                st.markdown(
                    f"<div class='salary-prediction'>"
                    f"Predicted Salary: ${predicted_salary:,.2f}"
                    f"</div>",
                    unsafe_allow_html=True
                )



if __name__ == '__main__':
    main()
