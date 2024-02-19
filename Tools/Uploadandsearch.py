# Import necessary libraries
from io import BytesIO, StringIO

import pandas as pd
import streamlit as st


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

            # Display the original dataframe in a table format
            st.dataframe(df)

            # Get list of column names for dropdown menu
            cols = df.columns.tolist()

            # Add a multiselect widget to select columns
            selected_cols = st.multiselect("Select Columns", cols)

            if len(selected_cols) > 0:
                # Get user input for search parameter
                search_param = st.text_input("Enter Search Parameter")

                # Add a button to filter dataframe
                if st.button("Filter"):
                    if search_param:  # If search parameter is not empty
                        filtered_df = df[
                            df[selected_cols].apply(
                                lambda x: str(x)
                                .lower()
                                .__contains__(search_param.lower()),
                                axis=1,
                            )
                        ]

                        # Display the filtered dataframe in a table format
                        st.dataframe(filtered_df)
                    else:  # If search parameter is empty, display original df
                        st.dataframe(df)
        except Exception as e:
            st.error("Error reading file: {}".format(e))


if __name__ == "__main__":
    main()
