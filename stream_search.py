import re

import pandas as pd
import requests
import streamlit as st

CSS_FILE = "style.css"
# Set page configuration to wide layout
st.set_page_config(
    page_title="Lookup Tool",
    initial_sidebar_state="expanded",
    layout="wide",
    page_icon="favicon.png",
)

CSS_FILE = "style.css"
# Apply custom CSS
with open(CSS_FILE) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Define a dictionary of sites to search
sites = {
    "Public APIs": {
        "url": ("https://api.publicapis.org/entries?title=", ""),
        "headers": {"Accept": "application/json"},
    },
    "CVE Lookup": {
        "url": ("https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=", ""),
        "headers": {"Accept": "application/json"},
    },
}


# Get user input
search_terms = st.text_input("Enter search terms (separated by spaces or commas): ")

# Add a drop-down for site selection
site_name = st.selectbox("Select a site to search:", list(sites.keys()))

if st.button("Search"):
    if search_terms:  # Check if search box is not empty
        # Initialize an empty DataFrame in session state
        st.session_state.df = pd.DataFrame()

        # Replace commas with spaces, then split on spaces
        if site_name == "CVE Lookup":
            # Keep hyphens for CVE Lookup
            search_terms = [
                re.sub(r"[^\w-]+", "", term.strip())
                for term in search_terms.replace(",", " ").split()
            ]
        else:
            search_terms = [
                re.sub(r"\W+", "", term.strip().lower())
                for term in search_terms.replace(",", " ").split()
            ]

        # Get the base URL and URL suffix for the selected site
        base_url, url_suffix = sites[site_name]["url"]
        headers = sites[site_name]["headers"]

        # Make the HTTP request
        for term in search_terms:
            with st.spinner(f'Searching for "{term}"...'):

                @st.cache_data
                def fetch_data(base_url, term, url_suffix, headers):
                    response = requests.get(
                        f"{base_url}{term}{url_suffix}", headers=headers
                    )
                    return response.json()

                    # Call the fetch_data function and assign its return value to data

            data = fetch_data(base_url, term, url_suffix, headers)

            if "vulnerabilities" in data:
                vulnerabilities = data["vulnerabilities"]

                data = []
                for vuln in vulnerabilities:
                    cve = vuln["cve"]
                    cve_id = cve["id"]
                    # source_identifier = cve["sourceIdentifier"]
                    published = cve["published"]
                    last_modified = cve["lastModified"]
                    descriptions = [
                        desc["value"]
                        for desc in cve["descriptions"]
                        if desc["lang"] == "en"
                    ]
                    description = descriptions[0] if descriptions else None
                    base_scores = [
                        metric["cvssData"]["baseScore"]
                        for metric in cve["metrics"]["cvssMetricV31"]
                    ]
                    base_score = base_scores[0] if base_scores else None

                data.append(
                    [
                        cve_id,
                        # source_identifier,
                        published,
                        # last_modified,
                        description,
                        base_score,
                    ]
                )

                # Create a DataFrame from the data
                new_df = pd.DataFrame(
                    data,
                    columns=[
                        "CVE ID",
                        # "Source Identifier",
                        "Published",
                        # "Last Modified",
                        "Description",
                        "Base Score",
                    ],
                )
            elif "entries" in data:
                pd.options.display.int_format = "{}".format
                new_df = pd.DataFrame(data["entries"])
            else:
                pd.options.display.int_format = "{}".format
                new_df = pd.DataFrame()

            # Check if the DataFrame is empty
            if new_df.empty:
                st.info(f"No results found for '{term}' on {site_name}.")
            else:
                # Concatenate the new data with the existing DataFrame
                st.session_state.df = pd.concat([st.session_state.df, new_df])
        # st.success("Search completed.")
    else:
        st.warning("Please enter at least one search term.")

# Check if DataFrame is not empty
if "df" in st.session_state and not st.session_state.df.empty:
    # Display the dataframe without the index
    st.dataframe(st.session_state.df, hide_index=True, use_container_width=True)

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
        # st.warning("No columns selected. Please select at least one column.")
        pass  # Placeholder indentation
    else:
        # Add a button for user validation
        if st.button("Generate Markdown"):
            # Convert selected columns of DataFrame to Markdown and allow user to copy it
            markdown = st.session_state.df[columns_to_export].to_markdown(index=False)
            st.text_area("Markdown Table", markdown, height=300)

            # Add a button to generate HTML
        if st.button("Generate HTML"):
            # Convert selected columns of DataFrame to HTML and allow user to copy it
            html = st.session_state.df[columns_to_export].to_html(index=False)
            st.text_area("HTML Table", html, height=300)
# Add a button to clear the search box
# if st.button("Clear Search Box"):
#    search_terms = ""
