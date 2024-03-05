import pandas as pd
import requests
import streamlit as st


# Define a function to retrieve CVE data from the NVD REST API
def get_cve_data(cve_ids):
    # Create a list to store the retrieved data
    cve_data = []

    # Loop through each CVE ID and retrieve the data
    for cve_id in cve_ids:
        url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
            data = response.json()

            # Extract the relevant fields from the JSON response
            for vuln in data.get("vulnerabilities", []):
                cve = vuln.get("cve", {})
                cvssData = (
                    cve.get("metrics", {})
                    .get("cvssMetricV31", [{}])[0]
                    .get("cvssData", {})
                )
                cve_data.append(
                    {
                        "CVE ID": cve.get("id", ""),
                        "Published": cve.get("published", ""),
                        "Last Modified": cve.get("lastModified", ""),
                        "Status": cve.get("vulnStatus", ""),
                        "Description": cve.get("descriptions", [{}])[0].get(
                            "value", ""
                        ),
                        "CVSS Score": cvssData.get("baseScore", ""),
                        "Severity": cvssData.get("baseSeverity", ""),
                        "Attack Vector": cvssData.get("attackVector", ""),
                        "Attack Complexity": cvssData.get("attackComplexity", ""),
                        "Privileges Required": cvssData.get("privilegesRequired", ""),
                        "User Interaction": cvssData.get("userInteraction", ""),
                        "Confidentiality Impact": cvssData.get(
                            "confidentialityImpact", ""
                        ),
                        "Integrity Impact": cvssData.get("integrityImpact", ""),
                        "Availability Impact": cvssData.get("availabilityImpact", ""),
                    }
                )
        except requests.exceptions.RequestException as e:
            st.write(f"Error retrieving CVE data for {cve_id}: {e}")

    # Return the retrieved data as a pandas DataFrame
    return pd.DataFrame(cve_data)

# Streamlit application
st.title("NVD CVE Data Retrieval")

# Input for CVE IDs
cve_ids_input = st.text_input("Enter CVE IDs (comma-separated):").upper()
cve_ids = [id.strip() for id in cve_ids_input.split(",")]

# Button to fetch data
if st.button("Fetch Data"):
    cve_data = get_cve_data(cve_ids)
    st.dataframe(cve_data)
