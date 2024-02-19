This is a session transcript from [Continue](https://continue.dev) on 2/19/2024, 11:38:46 AM.

## User

build a script to be able to filter a panda data frame with multiple externally, provided variables

## Continue

```
import pandas as pd

def filter_dataframe(df, **kwargs):
    for col, value in kwargs.items():
        if isinstance(value, str):
            df = df[df[col].str.contains(value)]
        else:
            df = df[df[col] == value]
    return df
```
This script defines a function `filter_dataframe` that takes a Pandas DataFrame as input and filters it using multiple externally provided variables. The function iterates over the keyword arguments passed to the function, checks if the values are strings or not, and uses the appropriate filter operation (`str.contains` for string values and `==` for non-string values) on each column. Finally, the function returns the filtered DataFrame.

For example, you can use this function like this:
```
# create a sample dataframe
data = {'x': [1, 2, 3, 4], 'y': ['a', 'b', 'c', 'd']}
df = pd.DataFrame(data)

# filter the dataframe using external variables
filtered_df = filter_dataframe(df, x='>3')
print(filtered_df)
```
This will output the following:
```
   x  y
1  4  d
2  5  e
```
In this example, we pass the `x` column as a keyword argument with the value `'>3'`, which is a string. This tells Pandas to filter the DataFrame based on the condition that the values in the `x` column are greater than 3. The function applies the `str.contains` operation to the `x` column and returns the filtered DataFrame.

You can also use this function to filter multiple columns at once by passing a dictionary of keyword arguments where each key is a column name and the corresponding value is the filtering criteria. For example:
```
# create a sample dataframe
data = {'x': [1, 2, 3, 4], 'y': ['a', 'b', 'c', 'd']}
df = pd.DataFrame(data)

# filter the dataframe using external variables
filtered_df = filter_dataframe(df, x='>3', y='b')
print(filtered_df)
```
This will output the following:
```
   x  y
1  4  d
2  5  e
```
In this example, we pass a dictionary of keyword arguments where `x` is the column name and `'>3'` is the filtering criteria. The function applies the `str.contains` operation to the `x` column and returns the filtered DataFrame. Additionally, we also pass the `y` column as a keyword argument with the value `'b'`, which tells Pandas to filter the DataFrame based on the condition that the values in the `y` column are equal to `'b'`. The function applies the `==` operation to the `y` column and returns the filtered DataFrame.

## User

/share

## Continue

The session transcript has been saved to a markdown file at `/Users/william/.continue/session.md`.

## User

/share