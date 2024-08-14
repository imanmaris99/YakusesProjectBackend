# # Base image
# FROM python:3.11-slim

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     python3-dev \
#     libpq-dev \
#     && apt-get clean

# # Set working directory
# WORKDIR /app

# # Copy project files
# COPY . .

# # Install Poetry
# RUN pip install poetry

# # Install dependencies
# RUN poetry install

# # Expose port
# EXPOSE 5000

# # Command to run the application
# CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0"]

# Use Python 3.11 as the base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock* /app/

# Install Poetry
RUN pip install poetry

# Install dependencies
RUN poetry install --no-root --no-dev

# Copy the rest of the application code
COPY . /app/

# Expose the port Uvicorn will run on
EXPOSE 5000

# Command to run the app using Uvicorn
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]

