
import pandas as pd


def transform_data(df):

    print("\nStarting data transformation...")

    # Remove completely empty rows
    df = df.dropna(how="all").copy()

    # Rename columns
    df = df.rename(columns={
        "Timestamp": "submitted_at",
        "Column 1": "first_name",
        "Surname": "surname",
        "Attendance Status": "raw_status",
        "Comments": "comments"
    })

    # Clean text fields
    text_columns = [
        "first_name",
        "surname",
        "raw_status",
        "comments"
    ]

    for col in text_columns:

        df[col] = (
            df[col]
            .astype("string")
            .str.strip()
            .replace("", pd.NA)
        )

    # Convert timestamps
    df["submitted_at"] = pd.to_datetime(
        df["submitted_at"],
        format="%m/%d/%Y %H:%M:%S",
        errors="coerce"
    )

    # Remove records missing required fields
    df = df.dropna(
        subset=[
            "submitted_at",
            "first_name",
            "surname",
            "raw_status"
        ]
    ).copy()

    # Standardise attendance status
    status_mapping = {
        "Sanlam Cape Town Office": "Present",
        "Leave": "Leave",
        "Sick Leave": "Sick Leave"
    }

    df["attendance_status"] = (
        df["raw_status"].map(status_mapping)
    )

    # Stop if an unknown status is found
    if df["attendance_status"].isna().any():

        raise ValueError(
            "Unknown attendance status found!"
        )

    # Assign office location
    df["location"] = df["raw_status"].map({
        "Sanlam Cape Town Office": "Sanlam Cape Town Office"
    })

    # Extract attendance date
    df["attendance_date"] = (
        df["submitted_at"].dt.date
    )

    # Remove duplicate employee/date records
    df = df.drop_duplicates(
        subset=[
            "first_name",
            "surname",
            "attendance_date"
        ],
        keep="last"
    )

    # Select final columns
    df = df[[
        "submitted_at",
        "first_name",
        "surname",
        "attendance_date",
        "attendance_status",
        "location",
        "comments"
    ]]

    print("Transformation completed!")
    print(f"Clean records: {len(df)}")

    return df
