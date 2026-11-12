
from dotenv import load_dotenv

from src.tracking import get_last_fetched_at
from src.extract import extract_data

load_dotenv()

# Get the previous fetch timestamp
last_fetch = get_last_fetched_at()

print("\nLast successful fetch:", last_fetch)

# Extract only new submissions
new_data = extract_data(last_fetched_at=last_fetch)

print("\nIncremental extraction results:")
print(f"New records found: {len(new_data)}")
