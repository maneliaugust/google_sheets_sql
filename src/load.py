
import os
import pandas as pd

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


def load_data(df):

    print("\nConnecting to PostgreSQL...")

    # Create database connection
    connection_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME")
    )

    engine = create_engine(connection_url)

    # Create attendance table
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

        CONSTRAINT unique_employee_attendance
        UNIQUE (first_name, surname, attendance_date),

        CONSTRAINT valid_attendance_status
        CHECK (
            attendance_status IN (
                'Present',
                'Leave',
                'Sick Leave'
            )
        )
    );
    """

    # Insert records
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

        ON CONFLICT (
            first_name,
            surname,
            attendance_date
        )

        DO UPDATE SET
            submitted_at = EXCLUDED.submitted_at,
            attendance_status = EXCLUDED.attendance_status,
            location = EXCLUDED.location,
            comments = EXCLUDED.comments;
    """)

    # Convert missing values to SQL NULL
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
