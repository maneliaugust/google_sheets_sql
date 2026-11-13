
from datetime import datetime

from dotenv import load_dotenv

from src.extract import extract_data
from src.transform import transform_data
from src.validate import validate_data
from src.load import load_data
from src.logger_config import setup_logger
from src.tracking import update_pipeline_tracking

from src.run_history import (
    create_run_history_table,
    start_pipeline_run,
    complete_pipeline_run,
    fail_pipeline_run
)


def run_pipeline():

    load_dotenv()

    logger = setup_logger()

    logger.info("Attendance ETL pipeline started")

    print("\n==============================")
    print("ATTENDANCE ETL PIPELINE")
    print("==============================")

    run_id = None

    try:

        # Create pipeline run history table
        create_run_history_table()

        # Record the start of this pipeline execution
        run_id = start_pipeline_run()

        fetched_at = datetime.now()

        # Step 1: Extract data
        raw_data = extract_data()

        logger.info(f"Extracted {len(raw_data)} rows")

        # Step 2: Transform data
        clean_data = transform_data(raw_data)

        logger.info(f"Transformed {len(clean_data)} clean records")

        # Step 3: Validate data
        validated_data = validate_data(clean_data)

        logger.info("Data quality validation passed")

        # Step 4: Load data into PostgreSQL
        load_data(validated_data)

        logger.info(f"Processed {len(validated_data)} records")

        # Step 5: Update existing pipeline tracking
        update_pipeline_tracking(
            records_fetched=len(raw_data),
            records_loaded=len(validated_data),
            fetched_at=fetched_at
        )

        # Step 6: Save successful pipeline run history
        complete_pipeline_run(
            run_id=run_id,
            records_fetched=len(raw_data),
            records_transformed=len(clean_data),
            records_loaded=len(validated_data),
            records_rejected=len(raw_data) - len(clean_data)
        )

        logger.info("Pipeline run history updated successfully")

        logger.info("Attendance ETL pipeline completed successfully")

        print("\n==============================")
        print("ETL PIPELINE COMPLETED")
        print("==============================")

    except Exception as error:

        logger.exception("ETL pipeline failed")

        # Record the failed execution
        if run_id is not None:

            try:
                fail_pipeline_run(
                    run_id=run_id,
                    error_message=str(error)
                )

            except Exception:
                logger.exception("Could not update failed pipeline run history")

        print("\nETL PIPELINE FAILED!")
        print("Check logs/pipeline.log for details.")

        raise


if __name__ == "__main__":
    run_pipeline()
