from io import BytesIO

import pandas as pd
import streamlit as st
from streamlit_condition_tree import condition_tree, config_from_dataframe


def main():
    # Set title for the app
    st.title("File Uploader")

    # Add a file upload widget
    uploaded_file = st.file_uploader(
        label="Choose a CSV or Excel file", type=["csv", "xls", "xlsx"]
    )

    if uploaded_file is not None:
        try:
            # Check the file extension to determine whether it's a csv or an excel file
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith((".xls", ".xlsx")):
                df = pd.read_excel(uploaded_file)
            # Basic field configuration from dataframe
            config = config_from_dataframe(df)

            # Condition tree
            query_string = condition_tree(config)

            # Filtered dataframe
            df = df.query(query_string)
        except Exception as e:
            st.error("Error reading file: {}".format(e))


if __name__ == "__main__":
    main()
