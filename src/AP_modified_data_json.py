import json

def transform_data(input_data):
    transformed_data = {}
    
    for law, states in input_data.items():
        transformed_data[law] = {}
        for state, value in states.items():
            transformed_data[law][state] = [
                {
                    "status": value,
                    "from": "2000-01-01",
                    "to": "2100-01-01"
                }
            ]
    
    return transformed_data

# Sample input data
input_data = {
  "goodsam-paroleyn": {
        "AL": 1,
        "AK": 1,
        "AZ": 1,
        "AR": 0,
        "CA": 1,
        "CO": 1,
        "CT": 1,
        "DE": 0,
        "DC": 0,
        "FL": 0,
        "GA": 0,
        "HI": 0,
        "ID": 1,
        "IL": 0,
        "IN": 1,
        "IA": 0,
        "KS": 0,
        "KY": 1,
        "LA": 0,
        "ME": 0,
        "MD": 0,
        "MA": 0,
        "MI": 1,
        "MN": 0,
        "MS": 0,
        "MO": 0,
        "MT": 0,
        "NE": 1,
        "NV": 0,
        "NH": 1,
        "NJ": 0,
        "NM": 0,
        "NY": 1,
        "NC": 0,
        "ND": 1,
        "OH": 0,
        "OK": 1,
        "OR": 0,
        "PA": 0,
        "RI": 0,
        "SC": 1,
        "SD": 1,
        "TN": 0,
        "TX": 1,
        "UT": 1,
        "VT": 0,
        "VA": 1,
        "WA": 1,
        "WV": 0,
        "WI": 1,
        "WY": 0
    },
    "goodsam-parole_Protection from arrest": {
        "AL": 0,
        "AK": 0,
        "AZ": 0,
        "AR": 0,
        "CA": 0,
        "CO": 0,
        "CT": 0,
        "DE": 0,
        "DC": 0,
        "FL": 0,
        "GA": 0,
        "HI": 0,
        "ID": 0,
        "IL": 0,
        "IN": 0,
        "IA": 0,
        "KS": 0,
        "KY": 0,
        "LA": 0,
        "ME": 0,
        "MD": 0,
        "MA": 0,
        "MI": 0,
        "MN": 0,
        "MS": 0,
        "MO": 0,
        "MT": 0,
        "NE": 0,
        "NV": 0,
        "NH": 0,
        "NJ": 0,
        "NM": 0,
        "NY": 0,
        "NC": 1,
        "ND": 0,
        "OH": 0,
        "OK": 0,
        "OR": 1,
        "PA": 0,
        "RI": 0,
        "SC": 0,
        "SD": 0,
        "TN": 0,
        "TX": 0,
        "UT": 0,
        "VT": 0,
        "VA": 0,
        "WA": 0,
        "WV": 0,
        "WI": 0,
        "WY": 0
    },
    "goodsam-parole_Protection from charge": {
        "AL": 0,
        "AK": 0,
        "AZ": 0,
        "AR": 0,
        "CA": 0,
        "CO": 0,
        "CT": 0,
        "DE": 0,
        "DC": 0,
        "FL": 0,
        "GA": 0,
        "HI": 0,
        "ID": 0,
        "IL": 0,
        "IN": 0,
        "IA": 0,
        "KS": 0,
        "KY": 0,
        "LA": 0,
        "ME": 0,
        "MD": 0,
        "MA": 0,
        "MI": 0,
        "MN": 0,
        "MS": 0,
        "MO": 0,
        "MT": 0,
        "NE": 0,
        "NV": 0,
        "NH": 0,
        "NJ": 0,
        "NM": 0,
        "NY": 0,
        "NC": 0,
        "ND": 0,
        "OH": 0,
        "OK": 0,
        "OR": 0,
        "PA": 1,
        "RI": 1,
        "SC": 0,
        "SD": 0,
        "TN": 0,
        "TX": 0,
        "UT": 0,
        "VT": 0,
        "VA": 0,
        "WA": 0,
        "WV": 0,
        "WI": 0,
        "WY": 0
    },
    "goodsam-parole_Protection from prosecution": {
        "AL": 0,
        "AK": 0,
        "AZ": 0,
        "AR": 0,
        "CA": 0,
        "CO": 0,
        "CT": 0,
        "DE": 0,
        "DC": 0,
        "FL": 0,
        "GA": 0,
        "HI": 0,
        "ID": 0,
        "IL": 0,
        "IN": 0,
        "IA": 0,
        "KS": 0,
        "KY": 0,
        "LA": 0,
        "ME": 0,
        "MD": 0,
        "MA": 0,
        "MI": 0,
        "MN": 0,
        "MS": 0,
        "MO": 0,
        "MT": 0,
        "NE": 0,
        "NV": 0,
        "NH": 0,
        "NJ": 0,
        "NM": 0,
        "NY": 0,
        "NC": 0,
        "ND": 0,
        "OH": 0,
        "OK": 0,
        "OR": 0,
        "PA": 1,
        "RI": 1,
        "SC": 0,
        "SD": 0,
        "TN": 0,
        "TX": 0,
        "UT": 0,
        "VT": 0,
        "VA": 0,
        "WA": 0,
        "WV": 0,
        "WI": 0,
        "WY": 0
    },
    "goodsam-parole_Protection from revocation of probation and\/or parole": {
        "AL": 0,
        "AK": 0,
        "AZ": 0,
        "AR": 0,
        "CA": 0,
        "CO": 0,
        "CT": 0,
        "DE": 1,
        "DC": 1,
        "FL": 0,
        "GA": 0,
        "HI": 0,
        "ID": 0,
        "IL": 0,
        "IN": 0,
        "IA": 1,
        "KS": 0,
        "KY": 0,
        "LA": 0,
        "ME": 1,
        "MD": 0,
        "MA": 0,
        "MI": 0,
        "MN": 1,
        "MS": 0,
        "MO": 0,
        "MT": 1,
        "NE": 0,
        "NV": 0,
        "NH": 0,
        "NJ": 1,
        "NM": 0,
        "NY": 0,
        "NC": 1,
        "ND": 0,
        "OH": 0,
        "OK": 0,
        "OR": 0,
        "PA": 0,
        "RI": 0,
        "SC": 0,
        "SD": 0,
        "TN": 0,
        "TX": 0,
        "UT": 0,
        "VT": 0,
        "VA": 0,
        "WA": 0,
        "WV": 0,
        "WI": 0,
        "WY": 0
    },
    "goodsam-parole_General protection from sanctions for violation of probation and\/or parole": {
        "AL": 0,
        "AK": 0,
        "AZ": 0,
        "AR": 1,
        "CA": 0,
        "CO": 0,
        "CT": 0,
        "DE": 0,
        "DC": 0,
        "FL": 1,
        "GA": 1,
        "HI": 1,
        "ID": 0,
        "IL": 1,
        "IN": 0,
        "IA": 0,
        "KS": 0,
        "KY": 0,
        "LA": 1,
        "ME": 0,
        "MD": 1,
        "MA": 1,
        "MI": 0,
        "MN": 0,
        "MS": 1,
        "MO": 1,
        "MT": 0,
        "NE": 0,
        "NV": 1,
        "NH": 0,
        "NJ": 0,
        "NM": 1,
        "NY": 0,
        "NC": 0,
        "ND": 0,
        "OH": 1,
        "OK": 0,
        "OR": 0,
        "PA": 0,
        "RI": 0,
        "SC": 0,
        "SD": 0,
        "TN": 1,
        "TX": 0,
        "UT": 0,
        "VT": 1,
        "VA": 0,
        "WA": 0,
        "WV": 1,
        "WI": 0,
        "WY": 0
    },
    "goodsam-mitigation": {
        "AL": 0,
        "AK": 1,
        "AZ": 1,
        "AR": 0,
        "CA": 0,
        "CO": 0,
        "CT": 0,
        "DE": 0,
        "DC": 1,
        "FL": 1,
        "GA": 0,
        "HI": 1,
        "ID": 0,
        "IL": 1,
        "IN": 1,
        "IA": 1,
        "KS": 0,
        "KY": 0,
        "LA": 1,
        "ME": 0,
        "MD": 1,
        "MA": 1,
        "MI": 0,
        "MN": 1,
        "MS": 0,
        "MO": 0,
        "MT": 1,
        "NE": 0,
        "NV": 1,
        "NH": 0,
        "NJ": 0,
        "NM": 1,
        "NY": 1,
        "NC": 0,
        "ND": 0,
        "OH": 0,
        "OK": 0,
        "OR": 0,
        "PA": 0,
        "RI": 1,
        "SC": 1,
        "SD": 1,
        "TN": 1,
        "TX": 0,
        "UT": 1,
        "VT": 1,
        "VA": 0,
        "WA": 1,
        "WV": 1,
        "WI": 0,
        "WY": 0
    },
    "goodsam-mit-type_Controlled substances offenses": {
        "AL": 0,
        "AK": 1,
        "AZ": 1,
        "AR": 0,
        "CA": 0,
        "CO": 0,
        "CT": 0,
        "DE": 0,
        "DC": 1,
        "FL": 1,
        "GA": 0,
        "HI": 1,
        "ID": 0,
        "IL": 1,
        "IN": 1,
        "IA": 1,
        "KS": 0,
        "KY": 0,
        "LA": 1,
        "ME": 0,
        "MD": 1,
        "MA": 1,
        "MI": 0,
        "MN": 1,
        "MS": 0,
        "MO": 0,
        "MT": 1,
        "NE": 0,
        "NV": 0,
        "NH": 0,
        "NJ": 0,
        "NM": 1,
        "NY": 1,
        "NC": 0,
        "ND": 0,
        "OH": 0,
        "OK": 0,
        "OR": 0,
        "PA": 0,
        "RI": 1,
        "SC": 1,
        "SD": 1,
        "TN": 1,
        "TX": 0,
        "UT": 1,
        "VT": 1,
        "VA": 0,
        "WA": 1,
        "WV": 1,
        "WI": 0,
        "WY": 0
    },
"temp": {
        "AL": 0,
        "AK": 0,
        "AZ": 0,
        "AR": 0,
        "CA": 0,
        "CO": 0,
        "CT": 0,
        "DE": 0,
        "DC": 0,
        "FL": 0,
        "GA": 0,
        "HI": 0,
        "ID": 0,
        "IL": 0,
        "IN": 0,
        "IA": 0,
        "KS": 0,
        "KY": 0,
        "LA": 0,
        "ME": 0,
        "MD": 0,
        "MA": 0,
        "MI": 0,
        "MN": 0,
        "MS": 0,
        "MO": 0,
        "MT": 0,
        "NE": 0,
        "NV": 0,
        "NH": 0,
        "NJ": 0,
        "NM": 0,
        "NY": 0,
        "NC": 0,
        "ND": 0,
        "OH": 0,
        "OK": 0,
        "OR": 0,
        "PA": 0,
        "RI": 0,
        "SC": 0,
        "SD": 0,
        "TN": 0,
        "TX": 0,
        "UT": 0,
        "VT": 0,
        "VA": 0,
        "WA": 0,
        "WV": 0,
        "WI": 0,
        "WY": 0
    },
    "goodsam-mit-type_Other offenses beyond controlled substances and alcohol-related violations": {
        "AL": 0,
        "AK": 0,
        "AZ": 0,
        "AR": 0,
        "CA": 0,
        "CO": 0,
        "CT": 0,
        "DE": 0,
        "DC": 0,
        "FL": 1,
        "GA": 0,
        "HI": 0,
        "ID": 0,
        "IL": 0,
        "IN": 0,
        "IA": 1,
        "KS": 0,
        "KY": 0,
        "LA": 0,
        "ME": 0,
        "MD": 1,
        "MA": 0,
        "MI": 0,
        "MN": 1,
        "MS": 0,
        "MO": 0,
        "MT": 1,
        "NE": 0,
        "NV": 1,
        "NH": 0,
        "NJ": 0,
        "NM": 1,
        "NY": 0,
        "NC": 0,
        "ND": 0,
        "OH": 0,
        "OK": 0,
        "OR": 0,
        "PA": 0,
        "RI": 0,
        "SC": 0,
        "SD": 1,
        "TN": 1,
        "TX": 0,
        "UT": 0,
        "VT": 1,
        "VA": 0,
        "WA": 1,
        "WV": 1,
        "WI": 0,
        "WY": 0
    }
}

# Transform the data
transformed_data = transform_data(input_data)

with open('transformed_laws.json', 'w') as json_file:
    json.dump(transformed_data, json_file, indent=2)


from sklearn.cluster import SpectralCoclustering
from matplotlib import colormaps
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
import matplotlib.colors as mcolors

import pandas as pd

original_df1 = pd.read_excel('SSP Update 2021 Data.xlsx')
original_df1 = original_df1.replace('.',0)

states = pd.read_csv('states.csv')  # Load the states.csv file

# Assuming states.csv has columns: 'State' and 'Abbreviation'
# Merge the DataFrames
merged_df = original_df1.merge(states, left_on='Jurisdictions', right_on='State', how='left')

# # Replace the 'jurisdictions' column with the abbreviations
original_df1['Jurisdictions'] = merged_df['Abbreviation']

# Drop any temporary columns if necessary
#merged_df.head()
original_df1.head(15)



import pandas as pd
import json

# Sample DataFrame setup (assuming original_df1 is your actual DataFrame)
# original_df1 = pd.read_excel("your_file.xlsx")  # Uncomment and load your DataFrame here

# Convert "Effective Date" and "Valid Through Date" to datetime (if not already done)
original_df1["Effective Date"] = pd.to_datetime(original_df1["Effective Date"], errors='coerce')
original_df1["Valid Through Date"] = pd.to_datetime(original_df1["Valid Through Date"], errors='coerce')

# Initialize the JSON structure
json_output = {}

# Iterate through each column (law) except "Jurisdictions", "Effective Date", and "Valid Through Date"
for column in original_df1.columns:
    if column in ["Jurisdictions", "Effective Date", "Valid Through Date"]:
        continue

    # Initialize the law in the JSON output
    if column not in json_output:
        json_output[column] = {}

    # Iterate through the DataFrame to populate each law
    for _, row in original_df1.iterrows():
        # Convert 'Effective Date' and 'Valid Through Date' to string for JSON compatibility
        effective_date_str = row["Effective Date"].strftime('%Y-%m-%d') if pd.notna(row["Effective Date"]) else None
        valid_through_date_str = row["Valid Through Date"].strftime('%Y-%m-%d') if pd.notna(row["Valid Through Date"]) else None
        
        # Add the jurisdiction data for the law
        if row["Jurisdictions"] not in json_output[column]:
            json_output[column][row["Jurisdictions"]] = [{
                "status": row[column],
                "from": effective_date_str,
                "to": valid_through_date_str
            }]
        else:
            json_output[column][row["Jurisdictions"]].append({
                "status": row[column],
                "from": effective_date_str,
                "to": valid_through_date_str
            })

# Convert dictionary to JSON string
output_json = json.dumps(json_output, indent=1)

# Print or save the JSON
print(output_json)


# Save JSON to file (ssp_file.json)
with open("ssp_file.json", "w") as json_file:
    json_file.write(output_json)

df1 = original_df1[["Jurisdictions", "Effective Date", "Valid Through Date"]]
df2 = df.drop(["Jurisdictions", "Effective Date", "Valid Through Date"], axis=1)

# Display the two DataFrames
print("First DataFrame:")
print(df1)
print("\nSecond DataFrame:")
print(df2)