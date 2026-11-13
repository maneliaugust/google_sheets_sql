
import os
import pandas as pd

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


def load_data(df):

    print("\nConnecting to PostgreSQL...")

    connection_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME")
    )

    engine = create_engine(connection_url)

    create_table = """
    CREATE TABLE IF NOT EXISTS attendance_records (
        id SERIAL PRIMARY KEY,
        submitted_at TIMESTAMP NOT NULL,
        first_name VARCHAR(100) NOT NULL,
        surname VARCHAR(100) NOT NULL,
        attendance_date DATE NOT NULL,
        attendance_status VARCHAR(30) NOT NULL,
        location VARCHAR(150),
        comments TEXT,
        first_detected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        last_updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

        CONSTRAINT unique_employee_attendance
        UNIQUE (first_name, surname, attendance_date),

        CONSTRAINT valid_attendance_status
        CHECK (attendance_status IN ('Present', 'Leave', 'Sick Leave'))
    );

    ALTER TABLE attendance_records
    ADD COLUMN IF NOT EXISTS first_detected_at
    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;

    ALTER TABLE attendance_records
    ADD COLUMN IF NOT EXISTS last_updated_at
    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;
    """

    insert_query = text("""
        INSERT INTO attendance_records (
            submitted_at,
            first_name,
            surname,
            attendance_date,
            attendance_status,
            location,
            comments
        )
        VALUES (
            :submitted_at,
            :first_name,
            :surname,
            :attendance_date,
            :attendance_status,
            :location,
            :comments
        )

        ON CONFLICT (first_name, surname, attendance_date)

        DO UPDATE SET
            submitted_at = EXCLUDED.submitted_at,
            attendance_status = EXCLUDED.attendance_status,
            location = EXCLUDED.location,
            comments = EXCLUDED.comments,
            last_updated_at = CURRENT_TIMESTAMP


        WHERE
            attendance_records.submitted_at IS DISTINCT FROM EXCLUDED.submitted_at
            OR attendance_records.attendance_status IS DISTINCT FROM EXCLUDED.attendance_status
            OR attendance_records.location IS DISTINCT FROM EXCLUDED.location
            OR attendance_records.comments IS DISTINCT FROM EXCLUDED.comments;
    """)

    records = (
        df.astype(object)
        .where(pd.notna(df), None)
        .to_dict(orient="records")
    )

    try:
        with engine.begin() as connection:

            connection.execute(text(create_table))

            if records:
                connection.execute(insert_query, records)

        print("Data successfully loaded!")
        print(f"Records processed: {len(records)}")

    finally:
        engine.dispose()
