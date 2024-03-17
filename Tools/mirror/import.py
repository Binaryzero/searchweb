import json
import os
import sqlite3


def connect_db(db_file):
    """Connect to the specified SQLite database."""
    conn = sqlite3.connect(db_file)
    return conn


def create_table(conn):
    """Create the CVE table if it doesn't already exist."""
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS cve_records
                      (cve_id TEXT PRIMARY KEY, data JSON)"""
    )
    conn.commit()


def read_json_file(file_path):
    """Read a JSON file and return its content."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def fetch_existing_data(conn, cve_id):
    """Fetch the existing data for a given CVE ID from the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT data FROM cve_records WHERE cve_id = ?", (cve_id,))
    result = cursor.fetchone()
    return result[0] if result else None


def update_or_insert_record(conn, cve_id, new_data_json):
    """Update an existing record or insert a new one."""
    existing_data_json = fetch_existing_data(conn, cve_id)
    if existing_data_json != new_data_json:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT OR REPLACE INTO cve_records (cve_id, data)
                          VALUES (?, ?)""",
            (cve_id, new_data_json),
        )
        conn.commit()


# Define the root directory containing JSON files
root_directory = "/Users/william/Code/searchtool/mirror"

# SQLite database file
db_file = "cve_database.db"

# Connect to the SQLite database and create table
conn = connect_db(db_file)
create_table(conn)

# Iterate over the directory tree
for dirpath, dirnames, filenames in os.walk(root_directory):
    for filename in filenames:
        if filename.endswith(".json"):
            file_path = os.path.join(dirpath, filename)
            data = read_json_file(file_path)
            cve_id = data.get("id")
            if cve_id:
                new_data_json = json.dumps(data)
                update_or_insert_record(conn, cve_id, new_data_json)

# Close the database connection
conn.close()
