import os

import pandas as pd

directory = "/path/to/directory"  # Replace with the actual directory path

# Get a sorted list of CSV filenames
csv_filenames = sorted(
    filename for filename in os.listdir(directory) if filename.endswith(".csv")
)

data_frames = []
for filename in csv_filenames:
    file_path = os.path.join(directory, filename)
    df = pd.read_csv(file_path)
    data_frames.append(df)

# Compare data frames
comparison_results = []
for i in range(len(data_frames) - 1):  # Subtract 1 to avoid going out of range
    df1 = data_frames[i]
    df2 = data_frames[i + 1]  # Compare with the next DataFrame
    total_items = len(df1) + len(df2)
    new_items = len(df2) - len(df1[df1.isin(df2)].dropna())
    removed_items = len(df1) - len(df2[df2.isin(df1)].dropna())
    comparison_results.append((i, i + 1, total_items, removed_items, new_items))

# Print comparison results
for result in comparison_results:
    print(f"Comparison between DataFrame {result[0]} and DataFrame {result[1]}:")
    print(f"Total items: {result[2]}")
    print(f"Removed items: {result[3]}")
    print(f"New items: {result[4]}")
    print()
