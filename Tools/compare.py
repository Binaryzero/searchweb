import os

import pandas as pd

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
    total_items_df1 = len(df1)
    total_items_df2 = len(df2)
    new_items_df = df2[~df2.isin(df1)].dropna()
    removed_items_df = df1[~df1.isin(df2)].dropna()

    new_items = len(new_items_df)
    removed_items = len(removed_items_df)
    comparison_results.append(
        (
            file_names[i],
            file_names[i + 1],
            total_items_df1,
            total_items_df2,
            removed_items,
            new_items,
        )
    )

# Print comparison results
for result in comparison_results:
    print(f"Comparison between {result[0]} and {result[1]}:")
    print(f"Total items in {result[0]}: {result[2]}")
    print(f"Total items in {result[1]}: {result[3]}")
    print(f"Removed items: {result[4]}")
    print(f"New items: {result[5]}\n")
