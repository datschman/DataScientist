import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests
import logging
import os

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
def display_salary_distribution(data, title):
    # Define custom salary ranges (bins) and labels
    bins = [0, 30000, 50000, 80000, 110000, float('inf')]
    labels = ['0-30k', '30-50k', '50-80k', '80-110k', '110k+']

    # Bin the salary data into the defined ranges
    data['salary_range'] = pd.cut(data['salary'], bins=bins, labels=labels, right=False)

    # Count the occurrences of each salary range
    salary_range_counts = data['salary_range'].value_counts().sort_index()

    # Plotting the number of occurrences of each salary range using a bar plot
    plt.figure(figsize=(7, 5))
    sns.barplot(x=salary_range_counts.index, y=salary_range_counts.values, palette=sns.light_palette("red", n_colors=5))
    plt.title(title, fontsize=16, color='#333333')
    plt.xlabel('Salary Range', fontsize=12, color='#333333')
    plt.ylabel('Number of Occurrences', fontsize=12, color='#333333')
    plt.xticks(rotation=45, color='#333333')
    plt.yticks(color='#333333')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(plt)

# Function to generate and display proportion of occurrences for each experience level by each job category
def display_experience_level_by_job(data):
    plt.figure(figsize=(7, 5))
    sns.countplot(data=data, x='job_title_cluster', hue='experience_level', palette=sns.color_palette("light:r", n_colors=4))
    plt.title('Proportion of Occurrences for Each Experience Level by Job Category', fontsize=16, color='#333333')
    plt.xlabel('Job Category', fontsize=12, color='#333333')
    plt.ylabel('Count', fontsize=12, color='#333333')
    plt.xticks(rotation=45, color='#333333')
    plt.yticks(color='#333333')
    plt.legend(title='Experience Level')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(plt)

# Function to generate and display the impact of experience level on salaries styled like the provided example
def display_experience_level_impact_on_salaries(data):
    plt.figure(figsize=(7, 5))
    sns.boxplot(data=data, x='experience_level', y='salary', palette=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"])
    plt.title('Impact of Experience Level on Salaries', fontsize=16, color='#333333')
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
            width: 150px;  /* Set the image width */
            margin-right: 20px;  /* Space between image and text */
        }
        .header-text {
            flex: 1;
            text-align: center;
        }
        .header-text h1 {
            margin-bottom: 0;
        }
        .centered-image img {
            width: 450px;  /* Triple the default width */
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
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="header-container">
            <img src="app/DaTaSciencelogo.png" alt="Data Science Career Navigator">
            <div class="header-text">
                <h1>Data Science Career Navigator</h1>
                <p>Predict your salary based on your experience level and other optional parameters.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        with st.form(key='salary_form'):
            experience_level_map = {'Entry-level': 'EN', 'Mid-level': 'MI', 'Senior-level': 'SE', 'Executive': 'EX'}
            employment_type_map = {'Full-time': 'FT', 'Part-time': 'PT', 'Contract': 'CT', 'Freelance': 'FL'}
            job_title_map = {'Data Science': 'Data Scien', 'Machine Learning': 'Machine Learning', 'Analytics': 'Analyst', 'Engineering': 'Engineer', 'Other Data job': 'Others'}
            location_map = {'US': 'US', 'GB': 'GB', 'CA': 'CA', 'ES': 'ES', 'IN': 'IN', 'DE': 'DE', 'FR': 'FR',
                            'Rest of Asia': 'Rest_of_Asia', 'Mexico and Latin America': 'Latin_America', 'Rest of the world': 'Rest_of_the_World', 'Rest of Europe': 'Rest_of_Europe'}
            remote_ratio_map = {'0%': 0, '50%': 50, '100%': 100}
            company_size_map = {'Small': 'S', 'Medium': 'M', 'Large': 'L'}

            work_year = 2024  # Assuming work_year is always 2024
            st.write("## Input your details")
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

            submit_button = st.form_submit_button(label='Predict Salary')

    if submit_button:
        predicted_salary = get_prediction(work_year, experience_level_map[experience_level], employment_type_map[employment_type],
                                          job_title_map[job_title_cluster], remote_ratio_map[remote_ratio],
                                          company_size, location_map[company_location_grouped])

        with col2:
            if isinstance(predicted_salary, str) and "Error" in predicted_salary:
                st.error(predicted_salary)
            else:
                st.markdown(
                    f"<div class='salary-prediction'>"
                    f"Predicted Salary: ${predicted_salary:,.2f}"
                    f"</div>",
                    unsafe_allow_html=True
                )

                # Load your dataset
                data_path = os.path.join(os.path.dirname(__file__), "../raw_data/ds_salaries.csv")
                data = pd.read_csv(data_path)

                # Add job_title_cluster column using the group_job_titles function
                data['job_title_cluster'] = data['job_title'].apply(group_job_titles)

                col2_1, col2_2, col2_3 = st.columns(3)

                # Filter the dataset and plot the graphs based on the experience level
                with col2_1:
                    if experience_level == 'Entry-level':
                        entry_level_data = data[data['experience_level'] == 'EN']
                        display_salary_distribution(entry_level_data, 'Salary Distribution for Entry-level / Junior')
                    elif experience_level == 'Mid-level':
                        mid_level_data = data[data['experience_level'] == 'MI']
                        display_salary_distribution(mid_level_data, 'Salary Distribution for Mid-level / Intermediate')
                    elif experience_level == 'Senior-level':
                        senior_level_data = data[data['experience_level'] == 'SE']
                        display_salary_distribution(senior_level_data, 'Salary Distribution for Senior-level')
                    elif experience_level == 'Executive':
                        executive_level_data = data[data['experience_level'] == 'EX']
                        display_salary_distribution(executive_level_data, 'Salary Distribution for Executive-level / Director')

                with col2_2:
                    display_experience_level_by_job(data)

                with col2_3:
                    display_experience_level_impact_on_salaries(data)

if __name__ == '__main__':
    main()
