import numpy as np
import pandas as pd

# First, let's create two sample dataframes
df1 = pd.DataFrame({"A": [1, 2, 3], "B": ["a", "b", "c"]})
df2 = pd.DataFrame({"A": [4, 5, 6], "C": ["d", "e", "f"]})

# We can combine the two dataframes using the merge function.
# We specify that we want to merge on the 'A' column and
# create a new column 'C' in the resulting dataframe
df = pd.merge(df1, df2, on="A", how="left")
# df["C"] = np.nan
df3 = df1 + df2
# The resulting dataframe will have all the columns from df1 and
# df2, including the new column 'C' with default value NaN.
print(df)
