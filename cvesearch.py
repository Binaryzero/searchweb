import requests
import pandas as pd
import streamlit as st

# URL of the GitHub repository
repo_url = "https://api.github.com/repos/CVEProject/cvelistV5/git/trees/main?recursive=1"

# Download the list of all files in the repository
response = requests.get(repo_url)
data = response.json()

# Filter the list to include only JSON files
json_files = [file for file in data["tree"] if file["path"].endswith(".json")]

# Download each JSON file and load the data into a pandas DataFrame
df = pd.DataFrame()
for file in json_files:
    file_url = f"https://raw.githubusercontent.com/CVEProject/cvelistV5/main/{file['path']}"
    response = requests.get(file_url)
    file_data = response.json()
    df = df.append(pd.json_normalize(file_data), ignore_index=True)

# Create a Streamlit search interface for the data
search_term = st.text_input("Enter a search term:")
if search_term:
    results = df[df.apply(lambda row: search_term in row.to_string(), axis=1)]
    st.dataframe(results)