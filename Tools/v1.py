from pprint import pprint
import requests
from bs4 import BeautifulSoup

client = NvdApiClient()
response = client.get_cpe_match(cve_id="CVE-2022-32223")

# Check if the request was successful (i.e., the CVE number exists)
if response.status_code == 200:
  # Parse the HTML content of the response into a BeautifulSoup object
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the table with the vulnerability details
    vulnerability_table = soup.find("table", {"class": "vuln-details"})

    # Iterate over the rows in the table and extract the data
    for row in vulnerability_table.find_all("tr"):
        # Extract the vulnerability information from each row
        cve_id, cwe_id, description, cvss_score = [td.text.strip() for td in row.find_all("td")]

        print(f"CVE ID: {cve_id}")
        print(f"CWE ID: {cwe_id}")
        print(f"Description: {description}")
        print(f"CVSS Score: {cvss_score}\n")
else:
    print("Error: CVE number not found.")
