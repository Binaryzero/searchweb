import streamlit as st
import sqlite3
import json
import pandas as pd

def connect_db(db_file='cve_database.db'):
    """Connect to the specified SQLite database."""
    return sqlite3.connect(db_file)

def fetch_cve_data(conn, cve_ids):
    """Fetch CVE data for given CVE IDs from the database and return as a list of dicts."""
    cve_data = []
    cursor = conn.cursor()
    for cve_id in cve_ids:
        cursor.execute('SELECT data FROM cve_records WHERE cve_id = ?', (cve_id,))
        result = cursor.fetchone()
        if result:
            data = json.loads(result[0])
            cve_data.append(data)
    return cve_data

def cve_data_to_dataframe(cve_data):
    """Convert CVE data to a Pandas DataFrame."""
    rows = []
    for data in cve_data:
        cwe = [w['description'][0]['value'] for w in data.get('weaknesses', []) if 'description' in w]
        rows.append({
            'CVE ID': data.get('id', 'N/A'),
            'Published': data.get('published', 'N/A'),
            'Last Modified': data.get('lastModified', 'N/A'),
            'Vulnerability Status': data.get('vulnStatus', 'N/A'),
            'Description (EN)': ' '.join([desc['value'] for desc in data.get('descriptions', []) if desc.get('lang') == 'en']),
            'Metrics': str(data.get('metrics', 'N/A')),
            'CWE': ', '.join(cwe) if cwe else 'N/A',
            'Configurations': str(data.get('configurations', 'N/A')),
        })
    return pd.DataFrame(rows)

def main():
    st.title('CVE Search Tool')
    cve_ids_input = st.text_area('Enter CVE IDs (comma-separated):', '')
    cve_ids = [cve_id.strip() for cve_id in cve_ids_input.split(',') if cve_id.strip()]

    if st.button('Search'):
        if cve_ids:
            with connect_db() as conn:
                cve_data = fetch_cve_data(conn, cve_ids)
                if cve_data:
                    df = cve_data_to_dataframe(cve_data)
                    st.dataframe(df)
                else:
                    st.error('No CVE IDs found in the database.')
        else:
            st.error('Please enter valid CVE IDs.')

if __name__ == '__main__':
    main()
