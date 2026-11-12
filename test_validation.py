
import pandas as pd
from dotenv import load_dotenv

from src.extract import extract_data
from src.transform import transform_data
from src.validate import validate_data

load_dotenv()

# Extract and transform the real data
raw_data = extract_data()
clean_data = transform_data(raw_data)

# Create a test copy
test_data = clean_data.copy()

# Introduce a duplicate attendance record
test_data = clean_data.copy()

test_data = pd.concat(
    [test_data, test_data.iloc[[0]]],
    ignore_index=True
)

# Test the validation
try:
    validate_data(test_data)

except ValueError as error:
    print("\nTest successful!")
    print("Invalid data was rejected:", error)

else:
    print("\nTest failed! Duplicate data was accepted.")
