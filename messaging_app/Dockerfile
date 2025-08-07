# Use Python base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the project files
COPY . .

# Expose Django's default port
EXPOSE 8000

# Start the Django app
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
