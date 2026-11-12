
from datetime import datetime

from dotenv import load_dotenv

from src.extract import extract_data
from src.transform import transform_data
from src.validate import validate_data
from src.load import load_data
from src.logger_config import setup_logger

from src.tracking import (
    get_last_fetched_at,
    update_pipeline_tracking
)


def run_pipeline():

    load_dotenv()

    logger = setup_logger()

    logger.info("Attendance ETL pipeline started")

    print("\n==============================")
    print("ATTENDANCE ETL PIPELINE")
    print("==============================")

    try:

        # GET LAST FETCH TIMESTAMP
        last_fetched_at = get_last_fetched_at()

        print("\nLast successful fetch:", last_fetched_at)

        # RECORD FETCH START TIME
        fetched_at = datetime.now()

        # EXTRACT
        raw_data = extract_data(
            last_fetched_at=last_fetched_at
        )

        logger.info(
            f"Extracted {len(raw_data)} new rows"
        )

        # TRANSFORM
        clean_data = transform_data(raw_data)

        logger.info(
            f"Transformed {len(clean_data)} clean records"
        )

        # VALIDATE
        validated_data = validate_data(clean_data)

        logger.info("Data quality validation passed")

        # LOAD
        load_data(validated_data)

        logger.info(
            f"Loaded {len(validated_data)} records into PostgreSQL"
        )

        # UPDATE TRACKING
        update_pipeline_tracking(
            records_fetched=len(raw_data),
            records_loaded=len(validated_data),
            fetched_at=fetched_at
        )

        logger.info("Pipeline tracking updated successfully")

        logger.info(
            "Attendance ETL pipeline completed successfully"
        )

        print("\n==============================")
        print("ETL PIPELINE COMPLETED")
        print("==============================")

    except Exception:

        logger.exception("ETL pipeline failed")

        print("\nETL PIPELINE FAILED!")
        print("Check logs/pipeline.log for details.")

        raise


if __name__ == "__main__":
    run_pipeline()
