from io import BytesIO

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

            cols = df.columns.tolist()

            selected_cols = st.multiselect("Select Columns", cols)

            if len(selected_cols) > 0:
                search_param = st.text_input("Enter Search Parameter")

                # Define filtered_df only when user clicks on "Filter" button
                filtered_df = df[
                    df[selected_cols].apply(
                        lambda x: str(x).lower().__contains__(search_param.lower()),
                        axis=1,
                    )
                ]

                if st.button("Filter"):
                    # Display the filtered dataframe in a table format
                    st.dataframe(filtered_df)

                if st.button("Export to Excel"):

                    # Convert the filtered DataFrame back to bytes, ready for download
                    with BytesIO() as buffer:
                        filtered_df.to_excel(buffer, index=False)
                        buffer.seek(0)

                        # Stream the contents of the file directly to the browser
                        st.download_button(
                            label="Download Excel File",
                            data=buffer,
                            file_name="filtered_dataframe.xlsx",
                        )
        except Exception as e:
            st.error("Error reading file: {}".format(e))


if __name__ == "__main__":
    main()
