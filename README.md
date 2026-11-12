# Google Sheets to PostgreSQL Attendance ETL Pipeline

## Project Overview

This project is an automated ETL (Extract, Transform, Load) pipeline that retrieves employee attendance records from Google Sheets, cleans and validates the data using Python and Pandas, and loads the processed records into a PostgreSQL database.

The purpose of the project is to demonstrate how data can be extracted from an external source, transformed into a consistent format, checked for quality, and stored in a relational database.

The pipeline also includes logging and incremental extraction to support monitoring and more efficient data processing.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Pandas | Data cleaning and transformation |
| Google Sheets API | Extracting attendance records |
| gspread | Connecting Python to Google Sheets |
| PostgreSQL | Storing processed attendance data |
| SQLAlchemy | Database connection and interaction |
| psycopg2 | PostgreSQL database driver |
| python-dotenv | Managing environment variables |
| Git and GitHub | Version control and project management |

## ETL Process

The pipeline follows three main stages:

### 1. Extract

- Connects to Google Sheets using Google service account credentials.
- Retrieves attendance records from the specified worksheet.
- Supports incremental extraction using the last successful fetch timestamp.

### 2. Transform

Uses Pandas to clean and prepare the extracted data.

The transformation process includes:

- Removing completely empty rows.
- Renaming columns into meaningful names.
- Removing unnecessary whitespace.
- Converting timestamps into the required format.
- Handling missing values in essential fields.
- Standardising attendance statuses.
- Creating an attendance date column.
- Removing duplicate employee attendance records.

### 3. Load

- Loads the cleaned records into PostgreSQL.
- Uses SQLAlchemy to interact with the database.
- Uses a unique employee and attendance date combination to prevent duplicate records.
- Uses an upsert approach to update existing records when necessary.

## Data Validation

The pipeline includes data quality checks to ensure that records meet the required conditions before loading.

Validation checks include:

- Required columns must be present.
- Essential fields must not contain missing values.
- Attendance statuses must match the accepted values.
- Duplicate employee attendance records are not allowed.

Accepted attendance statuses:

- Present
- Leave
- Sick Leave

## Logging and Pipeline Tracking

The project includes logging to record pipeline activities and errors.

Pipeline tracking is implemented using a PostgreSQL tracking table that stores information such as:

- Pipeline name.
- Last successful fetch timestamp.
- Last successful load timestamp.
- Number of records fetched.
- Number of records loaded.

This helps monitor pipeline execution and supports incremental data extraction.

## Project Structure

```text
google_sheets_postgres_attendance_etl/
│
├── src/
│   ├── __init__.py
│   ├── extract.py
│   ├── transform.py
│   ├── validate.py
│   ├── load.py
│   ├── tracking.py
│   ├── logger_config.py
│   └── main.py
│
|
|── test_connection.py
├── test_tracking.py
├── test_transform.py
└── test_validation.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

## How to Run the Project

### Prerequisites

Before running the project, make sure you have:

- Python 3.10 or later.
- PostgreSQL installed and running.
- A Google Cloud service account with Google Sheets API access.
- Access to a Google spreadsheet containing attendance records.

### 1. Clone the repository

```bash
git clone https://github.com/maneliaugust/google_sheets_sql.git
```

Navigate into the project folder:

```bash
cd google_sheets_sql
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\Activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root directory.

Add the following configuration:

```env
GOOGLE_SHEET_ID=your_google_sheet_id
GOOGLE_WORKSHEET_NAME=your_worksheet_name

DB_HOST=localhost
DB_PORT=5432
DB_NAME=attendance_db
DB_USER=postgres
DB_PASSWORD=your_database_password
```

Replace the example values with your own configuration.

### 5. Configure Google Sheets API access

- Enable the Google Sheets API in Google Cloud.
- Create a service account.
- Download its JSON credentials file.
- Place the file inside a `credentials/` folder.
- Share your Google spreadsheet with the service account email address.

The credentials file should be located at:

```text
credentials/credentials.json
```

**Important:** Never upload your `.env` file or Google service account credentials to GitHub.

### 6. Set up PostgreSQL

Make sure PostgreSQL is running and create a database named:

```sql
CREATE DATABASE attendance_db;
```

Ensure that the database connection details in your `.env` file are correct.

### 7. Run the ETL pipeline

From the project root directory, execute:

```bash
python -m src.main
```

The pipeline will extract, transform, validate and load the attendance records into PostgreSQL.

## Testing

The project includes separate test scripts for checking different components.

Run the tests individually:

```bash
python test_connection.py
python test_transform.py
python test_validation.py
python test_tracking.py
```