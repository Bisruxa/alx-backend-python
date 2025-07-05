# Python Generators – ALX Backend

This project demonstrates advanced usage of Python generators to efficiently process large datasets from a MySQL database.

## Tasks

- **Seed Database**: Creates `ALX_prodev` database and populates it from `user_data.csv`.
- **Stream Users**: Yields one user at a time from the database.
- **Batch Processing**: Fetches and filters users in batches.
- **Lazy Pagination**: Loads paginated user data using a generator.
- **Average Age**: Calculates average user age without loading all data into memory.

## Usage

```bash
python3 0-main.py       # Seed database
python3 1-main.py       # Stream users
python3 2-main.py       # Batch processing
python3 3-main.py       # Lazy pagination
python3 4-stream_ages.py  # Average age
