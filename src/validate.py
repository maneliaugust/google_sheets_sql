
def validate_data(df):

    print("\nStarting data quality validation...")

    # 1. Check required columns
    required_columns = [
        "submitted_at",
        "first_name",
        "surname",
        "attendance_date",
        "attendance_status",
        "location",
        "comments"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    # 2. Check required fields for missing values
    required_fields = [
        "submitted_at",
        "first_name",
        "surname",
        "attendance_date",
        "attendance_status"
    ]

    if df[required_fields].isnull().any().any():
        raise ValueError(
            "Required fields contain missing values!"
        )

    # 3. Check valid attendance statuses
    valid_statuses = [
        "Present",
        "Leave",
        "Sick Leave"
    ]

    invalid_statuses = df[
        ~df["attendance_status"].isin(valid_statuses)
    ]

    if not invalid_statuses.empty:
        raise ValueError(
            "Invalid attendance statuses found!"
        )

    # 4. Check duplicate employee attendance
    duplicates = df.duplicated(
        subset=[
            "first_name",
            "surname",
            "attendance_date"
        ]
    )

    if duplicates.any():
        raise ValueError(
            "Duplicate employee attendance records found!"
        )

    print("Data quality validation passed!")

    return df
