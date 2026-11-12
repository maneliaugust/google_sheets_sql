
from dotenv import load_dotenv

from src.extract import extract_data
from src.transform import transform_data

load_dotenv()

# Extract data
raw_data = extract_data()

# Transform data
clean_data = transform_data(raw_data)

# Display results
print("\nCleaned attendance records:")

print(clean_data.head(10).to_string(index=False))

# Check data types
print("\nData types:")

print(clean_data.dtypes)

# Check attendance breakdown
print("\nAttendance breakdown:")

print(
    clean_data["attendance_status"]
    .value_counts()
)

# Check missing values
print("\nMissing values:")

print(clean_data.isnull().sum())
