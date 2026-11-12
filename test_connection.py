
import os
import gspread

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Authenticate with Google
gc = gspread.service_account(
    filename="credentials/credentials.json"
)

# Open spreadsheet
spreadsheet = gc.open_by_key(
    os.getenv("GOOGLE_SHEET_ID")
)

print("Successfully connected to Google Sheets!")

# Display worksheet names
print("\nAvailable worksheets:")

for worksheet in spreadsheet.worksheets():
    print(worksheet.title)

# Access attendance responses
worksheet = spreadsheet.worksheet(
    os.getenv("GOOGLE_WORKSHEET_NAME")
)

# Retrieve records
records = worksheet.get_all_records()

print("\nTotal records retrieved:", len(records))

# Display column headings
print("\nColumn headings:")
print(worksheet.row_values(1))

# Display first five records
print("\nFirst five records:")

for record in records[:5]:
    print(record)
