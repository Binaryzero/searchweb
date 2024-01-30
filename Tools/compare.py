import os

import pandas as pd
from pandas import ExcelWriter

directory = "/path/to/directory"  # Replace with the actual directory path

# Get a sorted list of CSV filenames
csv_filenames = sorted(
    filename for filename in os.listdir(directory) if filename.endswith(".csv")
)

# Store filenames along with dataframes
data_frames = []
file_names = []
for filename in csv_filenames:
    file_path = os.path.join(directory, filename)
    df = pd.read_csv(file_path)
    data_frames.append(df)
    file_names.append(filename)

# Compare data frames
comparison_results = []
for i in range(len(data_frames) - 1):  # Subtract 1 to avoid going out of range
    df1 = data_frames[i]
    df2 = data_frames[i + 1]  # Compare with the next DataFrame
    total_items = len(df1) + len(df2)

    # Merge the dataframes and mark the source of each row
    merged_df = pd.merge(df1, df2, how="outer", indicator=True)

    # Find new and removed items
    new_items_df = merged_df[merged_df["_merge"] == "right_only"]
    removed_items_df = merged_df[merged_df["_merge"] == "left_only"]

    # Save the details of the removed and new items to separate worksheets in an Excel file
    with ExcelWriter(f"Difference{file_names[i]}-{file_names[i + 1]}.xlsx") as writer:
        new_items_df.to_excel(writer, sheet_name="New Items", index=False)
        removed_items_df.to_excel(writer, sheet_name="Removed Items", index=False)

    new_items = len(new_items_df)
    removed_items = len(removed_items_df)
    comparison_results.append(
        (file_names[i], file_names[i + 1], total_items, removed_items, new_items)
    )
# Print comparison results
for result in comparison_results:
    print(f"Comparison between {result[0]} and {result[1]}:")
    print(f"Total items: {result[2]}")
    print(f"Removed items: {result[3]}")
    print(f"New items: {result[4]}\n")
