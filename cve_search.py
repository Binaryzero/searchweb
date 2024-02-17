from typing import List

import requests
import streamlit as st


def search_nvd(cve_id, product, vendor):
    if cve_id is not None:
        url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cve_id={cve_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["CVE_Items"]
        else:
            print("Error: Could not retrieve search results from NVD API.")
            return None
    elif product is not None:
        url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?product={product}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["CVE_Items"]
        else:
            print("Error: Could not retrieve search results from NVD API.")
            return None
    elif vendor is not None:
        url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?vendor={vendor}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["CVE_Items"]
        else:
            print("Error: Could not retrieve search results from NVD API.")
            return None
    else:
        return None


st.title("NVD Vulnerability Search")

cve_id = st.text_input("CVE ID", "")
product = st.text_input("Product Name", "")
vendor = st.text_input("Vendor Name", "")

results = search_nvd(cve_id, product, vendor)

if results is not None:
    st.table(results)
else:
    st.write("No results found.")
