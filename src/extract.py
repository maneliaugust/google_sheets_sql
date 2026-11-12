
import os
import gspread
import pandas as pd


def extract_data(last_fetched_at=None):

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

    print(f"Total rows retrieved: {len(df)}")

    # Filter records using the last fetched timestamp
    if last_fetched_at is not None and not df.empty:

        timestamps = pd.to_datetime(
            df["Timestamp"],
            format="%m/%d/%Y %H:%M:%S",
            errors="coerce"
        )

        df = df[timestamps >= last_fetched_at].copy()

    print("Extraction completed!")
    print(f"New rows retrieved: {len(df)}")

    return df
