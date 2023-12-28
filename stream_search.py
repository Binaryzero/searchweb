import re

import pandas as pd
import requests
import streamlit as st

# Set page configuration to wide layout
st.set_page_config(
   page_title="Lookup Tool",
   initial_sidebar_state="expanded",
   layout="wide",
)
# Define a dictionary of sites to search
sites = {
    "Public APIs": ("https://api.publicapis.org/entries?title=", ""),
    "Random Public APIs": ("https://api.publicapis.org/random?title=", ""),
}

# Add a drop-down for site selection in the sidebar
site_name = st.sidebar.selectbox("Select a site to search:", list(sites.keys()))

# Get user input
search_terms = st.text_input("Enter search terms (separated by spaces or commas): ")

if st.sidebar.button("Search"):
    if search_terms:  # Check if search box is not empty
        # Initialize an empty DataFrame in session state
        st.session_state.df = pd.DataFrame()

        # Replace commas with spaces, then split on spaces
        search_terms = [re.sub(r'\W+', '', term.strip().lower()) for term in search_terms.replace(',', ' ').split()]

        # ...
        with st.spinner("Searching..."):  # Display a loading spinner
            for term in search_terms:
                # Send GET request to the selected site
                base_url, url_suffix = sites[site_name]
                try:
                    response = requests.get(f"{base_url}{term}{url_suffix}")
                    response.raise_for_status()  # Raises stored HTTPError, if one occurred.
                except requests.exceptions.HTTPError as http_err:
                    st.error(f"HTTP error occurred: {http_err}")
                except requests.exceptions.RequestException as err:
                    st.error(f"An error occurred: {err}")
                else:
                    # Load response into DataFrame
                    data = response.json()
                    new_df = pd.DataFrame(data["entries"])

                    # Check if the DataFrame is empty
                    if new_df.empty:
                        st.info(f"No results found for '{term}' on {site_name}.")
                    else:
                        # Concatenate the new data with the existing DataFrame
                        st.session_state.df = pd.concat([st.session_state.df, new_df])
        st.success("Search completed.")
    else:
        st.warning("Please enter at least one search term.")

# Check if DataFrame is not empty
if "df" in st.session_state and not st.session_state.df.empty:
    # Display the dataframe without the index
    st.dataframe(st.session_state.df, hide_index=True)

    # Create a list of columns
    columns = st.columns(len(st.session_state.df.columns.tolist()) + 1)

    # Initialize an empty list to store selected columns
    columns_to_export = []

    # Create a "Select All" checkbox
    if columns[0].checkbox("Select All"):
        columns_to_export = st.session_state.df.columns.tolist()
    else:
        # Create a checkbox in each column
        for i, col in enumerate(st.session_state.df.columns.tolist()):
            if columns[i + 1].checkbox(col):
                columns_to_export.append(col)

    # Check if any column is selected
    if not columns_to_export:
        st.warning("No columns selected. Please select at least one column.")
    else:
        # Add a button for user validation
        if st.sidebar.button("Generate Markdown"):
            # Convert selected columns of DataFrame to Markdown and allow user to copy it
            markdown = st.session_state.df[columns_to_export].to_markdown()
            st.text_area("Markdown Table", markdown, height=300)
else:
    st.warning("No data available. Please perform a search first.")
