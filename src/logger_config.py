
import logging
import os


def setup_logger():

    # Create logs folder if it does not exist
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        filename="logs/pipeline.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8"
    )

    logger = logging.getLogger("attendance_pipeline")

    return logger
