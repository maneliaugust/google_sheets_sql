
import os

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


def get_engine():

    connection_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME")
    )

    return create_engine(connection_url)


def create_run_history_table():

    engine = get_engine()

    create_table_query = text("""
        CREATE TABLE IF NOT EXISTS pipeline_run_history (
            run_id SERIAL PRIMARY KEY,
            pipeline_name VARCHAR(100) NOT NULL,
            started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            records_fetched INTEGER DEFAULT 0,
            records_transformed INTEGER DEFAULT 0,
            records_loaded INTEGER DEFAULT 0,
            records_rejected INTEGER DEFAULT 0,
            status VARCHAR(20) NOT NULL DEFAULT 'Running',
            error_message TEXT,

            CONSTRAINT valid_run_status
            CHECK (status IN ('Running', 'Success', 'Failed'))
        );
    """)

    try:
        with engine.begin() as connection:
            connection.execute(create_table_query)

        print("Pipeline run history table ready!")

    finally:
        engine.dispose()


def start_pipeline_run():

    engine = get_engine()

    query = text("""
        INSERT INTO pipeline_run_history (
            pipeline_name,
            status
        )
        VALUES (
            'Attendance ETL Pipeline',
            'Running'
        )
        RETURNING run_id;
    """)

    try:
        with engine.begin() as connection:
            result = connection.execute(query)
            run_id = result.scalar_one()

        print(f"Pipeline run started. Run ID: {run_id}")

        return run_id

    finally:
        engine.dispose()


def complete_pipeline_run(
    run_id,
    records_fetched,
    records_transformed,
    records_loaded,
    records_rejected
):

    engine = get_engine()

    query = text("""
        UPDATE pipeline_run_history
        SET
            completed_at = CURRENT_TIMESTAMP,
            records_fetched = :records_fetched,
            records_transformed = :records_transformed,
            records_loaded = :records_loaded,
            records_rejected = :records_rejected,
            status = 'Success'
        WHERE run_id = :run_id;
    """)

    try:
        with engine.begin() as connection:
            connection.execute(query, {
                "run_id": run_id,
                "records_fetched": records_fetched,
                "records_transformed": records_transformed,
                "records_loaded": records_loaded,
                "records_rejected": records_rejected
            })

        print("Pipeline run history saved successfully!")

    finally:
        engine.dispose()


def fail_pipeline_run(run_id, error_message):

    engine = get_engine()

    query = text("""
        UPDATE pipeline_run_history
        SET
            completed_at = CURRENT_TIMESTAMP,
            status = 'Failed',
            error_message = :error_message
        WHERE run_id = :run_id;
    """)

    try:
        with engine.begin() as connection:
            connection.execute(query, {
                "run_id": run_id,
                "error_message": str(error_message)
            })

        print("Failed pipeline run recorded!")

    finally:
        engine.dispose()
