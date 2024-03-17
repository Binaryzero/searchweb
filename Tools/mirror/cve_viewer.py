import json
import sqlite3

import pandas as pd
import streamlit as st


def connect_db(db_file):
    """Connect to the specified SQLite database."""
    return sqlite3.connect(db_file)


def fetch_cve_data(conn, cve_id):
    """Fetch CVE data for a given CVE ID from the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT data FROM cve_records WHERE cve_id = ?", (cve_id,))
    result = cursor.fetchone()
    return json.loads(result[0]) if result else None


def compile_data_to_dataframe(cve_ids, conn):
    """Compile CVE data into a Pandas DataFrame."""
    data_rows = []

    for cve_id in cve_ids:
        data = fetch_cve_data(conn, cve_id)
        if data:
            row = {
                "CVE ID": data.get("id", "N/A"),
                "Published": data.get("published", "N/A"),
                "Last Modified": data.get("lastModified", "N/A"),
                "Vulnerability Status": data.get("vulnStatus", "N/A"),
                "Description": " ".join(
                    [
                        desc["value"]
                        for desc in data.get("descriptions", [])
                        if desc.get("lang") == "en"
                    ]
                ),
                "Metrics": str(data.get("metrics", "N/A")),
                "Weaknesses": str(data.get("weaknesses", "N/A")),
                "Configurations": str(data.get("configurations", "N/A")),
            }
            data_rows.append(row)

    df = pd.DataFrame(data_rows)
    return df


def main():
    # SQLite database file
    db_file = "cve_database.db"

    # Connect to the SQLite database
    conn = connect_db(db_file)

    # Streamlit page setup
    st.title("CVE Search Tool")
    cve_ids_input = st.text_area("Enter CVE IDs (comma-separated):", "")
    cve_ids = [cve_id.strip() for cve_id in cve_ids_input.split(",") if cve_id.strip()]

    if st.button("Search"):
        if cve_ids:
            df = compile_data_to_dataframe(cve_ids, conn)
            if not df.empty:
                st.dataframe(df)
            else:
                st.error("No CVE IDs found in the database.")
        else:
            st.error("Please enter valid CVE IDs.")

    # Close the database connection
    conn.close()


if __name__ == "__main__":
    main()
