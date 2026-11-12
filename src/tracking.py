
import os

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


def update_pipeline_tracking(
    records_fetched,
    records_loaded,
    fetched_at
):

    connection_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME")
    )

    engine = create_engine(connection_url)

    query = text("""
    INSERT INTO pipeline_tracking (
        pipeline_name,
        last_fetched_at,
        last_loaded_at,
        records_fetched,
        records_loaded
    )
        VALUES (
        'Attendance ETL Pipeline',
        :fetched_at,
        CURRENT_TIMESTAMP,
        :records_fetched,
        :records_loaded
    )

    ON CONFLICT (pipeline_name)
    DO UPDATE SET
        last_fetched_at = EXCLUDED.last_fetched_at,
        last_loaded_at = CURRENT_TIMESTAMP,
        records_fetched = EXCLUDED.records_fetched,
        records_loaded = EXCLUDED.records_loaded;
""")

    try:
        with engine.begin() as connection:
            connection.execute(
                query,
                {
                    "records_fetched": records_fetched,
                    "records_loaded": records_loaded,
                    "fetched_at": fetched_at
                }
            )

        print("Pipeline tracking updated successfully!")

    finally:
        engine.dispose()

def get_last_fetched_at():

    connection_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME")
    )

    engine = create_engine(connection_url)

    query = text("""
        SELECT last_fetched_at
        FROM pipeline_tracking
        WHERE pipeline_name = 'Attendance ETL Pipeline';
    """)

    try:
        with engine.connect() as connection:

            result = connection.execute(query)

            row = result.fetchone()

            if row:
                return row[0]

            return None

    finally:
        engine.dispose()
