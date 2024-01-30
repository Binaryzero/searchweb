# Step 1: Import pandas
import pandas as pd

# Step 2: Create a DataFrame
data = {
    'fruit': ['apple', 'banana', 'apple', 'banana', 'apple', 'banana'],
    'customer': ['John', 'John', 'Steve', 'Steve', 'Ben', 'Ben'],
    'quantity': [5, 2, 5, 7, 6, 8]
}
df = pd.DataFrame(data)

# Step 3: Create a pivot table
pivot_table = df.pivot_table(index='customer', columns='fruit', values='quantity', aggfunc='count')