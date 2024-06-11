import pandas as pd

#Changing the structure : loading directly into the models.py file
#data = pd.read_csv("../raw_data/ds_salaries.csv")

#delete duplicate
def delete_duplicates (data):
    data = data.drop_duplicates()
    return data

#Group Job titles
def group_job_titles(data):
    job_titles = data["job_title"].unique()

    # keywords
    keywords = ["Data Scien",  "Machine Learning", "Analyst" , "Engineer" ]
    # old list long: keywords = ["Data Scien",  "Machine Learning", "Analyst", "Engineer", "Research", "Analytics", "Vision", "Architect", "Developer", "Manager", "Head", "Lead", "Cloud", "Specialist", "Principal"]


    # create dictionary
    clusters = {keyword: [] for keyword in keywords}
    clusters["Others"] = []

    # assign job titles
    for title in job_titles:
        matched = False
        for keyword in keywords:
            if keyword.lower() in title.lower():
                clusters[keyword].append(title)
                matched = True
        if not matched:
            clusters["Others"].append(title)

    #Assign cluster in new column
    def assign_cluster(title):
        for keyword in keywords:
            if keyword.lower() in title.lower():
                return keyword
        return "Others"

    data['job_title_cluster'] = data['job_title'].apply(assign_cluster)
    return data
    #print(data['job_title_cluster'])


#Group Countries by regions
def group_countries(data):


    # List of countries with more than 30 entries
    high_entry_countries = ['US', 'GB', 'CA', 'ES', 'IN', 'DE', 'FR']

    # Create a dictionary mapping each country to its region
    country_to_region = {
    'NG': 'Rest_of_the_World', 'GH': 'Rest_of_the_World', 'KE': 'Rest_of_the_World', 'EG': 'Rest_of_the_World', 'DZ': 'Rest_of_the_World',
    'MA': 'Rest_of_the_World', 'ZA': 'Rest_of_the_World', 'AO': 'Rest_of_the_World', 'TN': 'Rest_of_the_World', 'CI': 'Rest_of_the_World',
    'CM': 'Rest_of_the_World', 'ET': 'Rest_of_the_World', 'SN': 'Rest_of_the_World', 'UG': 'Rest_of_the_World', 'TZ': 'Rest_of_the_World',
    'CD': 'Rest_of_the_World', 'ZW': 'Rest_of_the_World', 'MZ': 'Rest_of_the_World', 'NE': 'Rest_of_the_World', 'MW': 'Rest_of_the_World',
    'BJ': 'Rest_of_the_World', 'BF': 'Rest_of_the_World', 'ML': 'Rest_of_the_World', 'GN': 'Rest_of_the_World', 'TD': 'Rest_of_the_World',
    'SO': 'Rest_of_the_World', 'BI': 'Rest_of_the_World', 'LS': 'Rest_of_the_World', 'ER': 'Rest_of_the_World', 'LY': 'Rest_of_the_World',
    'NA': 'Rest_of_the_World', 'GQ': 'Rest_of_the_World', 'GW': 'Rest_of_the_World', 'SS': 'Rest_of_the_World', 'GA': 'Rest_of_the_World',
    'SL': 'Rest_of_the_World', 'CG': 'Rest_of_the_World', 'SZ': 'Rest_of_the_World', 'RE': 'Rest_of_the_World', 'ST': 'Rest_of_the_World',
    'YT': 'Rest_of_the_World', 'SC': 'Rest_of_the_World', 'ZM': 'Rest_of_the_World', 'BW': 'Rest_of_the_World', 'CV': 'Rest_of_the_World',
    'MU': 'Rest_of_the_World', 'KM': 'Rest_of_the_World', 'GM': 'Rest_of_the_World', 'GW': 'Rest_of_the_World', 'TG': 'Rest_of_the_World',
    'BJ': 'Rest_of_the_World', 'AO': 'Rest_of_the_World', 'MW': 'Rest_of_the_World', 'ZW': 'Rest_of_the_World', 'CD': 'Rest_of_the_World',
    'HK': 'Rest_of_Asia', 'SG': 'Rest_of_Asia', 'TH': 'Rest_of_Asia', 'VN': 'Rest_of_Asia', 'MY': 'Rest_of_Asia',
    'PH': 'Rest_of_Asia', 'ID': 'Rest_of_Asia', 'JP': 'Rest_of_Asia', 'CN': 'Rest_of_Asia', 'KR': 'Rest_of_Asia',
    'TW': 'Rest_of_Asia', 'PK': 'Rest_of_Asia', 'BD': 'Rest_of_Asia', 'LK': 'Rest_of_Asia',
    'NP': 'Rest_of_Asia', 'MM': 'Rest_of_Asia', 'KH': 'Rest_of_Asia', 'BN': 'Rest_of_Asia', 'TL': 'Rest_of_Asia',
    'MN': 'Rest_of_Asia', 'UZ': 'Rest_of_Asia', 'TM': 'Rest_of_Asia', 'KG': 'Rest_of_Asia', 'TJ': 'Rest_of_Asia',
    'AZ': 'Rest_of_Asia', 'GE': 'Rest_of_Asia', 'AM': 'Rest_of_Asia', 'SY': 'Rest_of_Asia', 'IQ': 'Rest_of_Asia',
    'LB': 'Rest_of_Asia', 'JO': 'Rest_of_Asia', 'PS': 'Rest_of_Asia', 'KW': 'Rest_of_Asia', 'SA': 'Rest_of_Asia',
    'OM': 'Rest_of_Asia', 'YE': 'Rest_of_Asia', 'AE': 'Rest_of_Asia', 'QA': 'Rest_of_Asia', 'BH': 'Rest_of_Asia',
    'IR': 'Rest_of_Asia', 'AF': 'Rest_of_Asia', 'TL': 'Rest_of_Asia', 'MV': 'Rest_of_Asia', 'BT': 'Rest_of_Asia',
    'AR': 'Latin_America', 'BO': 'Latin_America', 'BR': 'Latin_America', 'CL': 'Latin_America',
    'CO': 'Latin_America', 'EC': 'Latin_America', 'FK': 'Latin_America', 'GF': 'Latin_America',
    'GY': 'Latin_America', 'PE': 'Latin_America', 'PY': 'Latin_America', 'SR': 'Latin_America',
    'UY': 'Latin_America', 'VE': 'Latin_America', 'MX': 'Latin_America', 'CR': 'Latin_America',
    'DO': 'Latin_America', 'GT': 'Latin_America', 'HN': 'Latin_America', 'NI': 'Latin_America',
    'PA': 'Latin_America', 'SV': 'Latin_America', 'BZ': 'Latin_America', 'BB': 'Latin_America',
    'CU': 'Latin_America', 'JM': 'Latin_America', 'HT': 'Latin_America', 'TT': 'Latin_America',
    'BS': 'Latin_America', 'LC': 'Latin_America', 'GD': 'Latin_America', 'AG': 'Latin_America',
    'DM': 'Latin_America', 'VC': 'Latin_America', 'KN': 'Latin_America',
    'AU': 'Rest_of_the_World', 'FJ': 'Rest_of_the_World', 'KI': 'Rest_of_the_World', 'MH': 'Rest_of_the_World', 'FM': 'Rest_of_the_World',
    'NR': 'Rest_of_the_World', 'NZ': 'Rest_of_the_World', 'PW': 'Rest_of_the_World', 'PG': 'Rest_of_the_World', 'WS': 'Rest_of_the_World',
    'SB': 'Rest_of_the_World', 'TO': 'Rest_of_the_World', 'TV': 'Rest_of_the_World', 'VU': 'Rest_of_the_World',
    'AT': 'Rest_of_Europe', 'BE': 'Rest_of_Europe', 'BG': 'Rest_of_Europe', 'HR': 'Rest_of_Europe', 'CY': 'Rest_of_Europe',
    'CZ': 'Rest_of_Europe', 'DK': 'Rest_of_Europe', 'EE': 'Rest_of_Europe', 'FI': 'Rest_of_Europe',
    'GR': 'Rest_of_Europe', 'HU': 'Rest_of_Europe', 'IS': 'Rest_of_Europe', 'IE': 'Rest_of_Europe',
    'IT': 'Rest_of_Europe', 'LV': 'Rest_of_Europe', 'LT': 'Rest_of_Europe', 'LU': 'Rest_of_Europe', 'MT': 'Rest_of_Europe',
    'NL': 'Rest_of_Europe', 'NO': 'Rest_of_Europe', 'PL': 'Rest_of_Europe', 'PT': 'Rest_of_Europe', 'RO': 'Rest_of_Europe',
    'RU': 'Rest_of_Europe', 'SK': 'Rest_of_Europe', 'SI': 'Rest_of_Europe', 'SE': 'Rest_of_Europe',
    'CH': 'Rest_of_Europe', 'UA': 'Rest_of_Europe', 'RS': 'Rest_of_Europe', 'MD': 'Rest_of_Europe',
    'ME': 'Rest_of_Europe', 'MK': 'Rest_of_Europe', 'AL': 'Rest_of_Europe', 'BA': 'Rest_of_Europe', 'XK': 'Rest_of_Europe',
    'BY': 'Rest_of_Europe', 'AD': 'Rest_of_Europe', 'MC': 'Rest_of_Europe', 'SM': 'Rest_of_Europe', 'LI': 'Rest_of_Europe',
    'VA': 'Rest_of_Europe'
    }
    # Ensure countries with high entries remain their own category
    for country in high_entry_countries:
        country_to_region[country] = country

    # Function to map company location to regions or keep it unchanged for high entry countries
    def map_location(location):
        if location in high_entry_countries:
            return location
        return country_to_region.get(location, 'Rest_of_the_World')  # Default to 'Rest_of_the_World' if not found in the dictionary

    # Create the new column company_location_grouped
    data['company_location_grouped'] = data['company_location'].apply(map_location)

    # Count the number of entries for each region and high-entry country
    region_counts = data['company_location_grouped'].value_counts()
    #print(region_counts)
    return data
