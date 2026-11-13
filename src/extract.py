
import os
import gspread
import pandas as pd


def extract_data():

    print("\nConnecting to Google Sheets...")

    gc = gspread.service_account(
        filename="credentials/credentials.json"
    )

    spreadsheet = gc.open_by_key(
        os.getenv("GOOGLE_SHEET_ID")
    )

    worksheet = spreadsheet.worksheet(
        os.getenv("GOOGLE_WORKSHEET_NAME")
    )

    records = worksheet.get_all_records()

    df = pd.DataFrame(records)

    print("Extraction completed!")
    print(f"Total rows retrieved: {len(df)}")

    return df
