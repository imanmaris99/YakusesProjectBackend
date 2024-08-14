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

# Gunakan Python 3.11 sebagai base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Salin file requirements
COPY pyproject.toml poetry.lock* /app/

# Install Poetry
RUN pip install poetry

# Install dependencies
RUN poetry install --no-root --no-dev

# Salin sisa kode aplikasi
COPY . /app/

# Expose port
EXPOSE 5000

# Command to run the app
CMD ["poetry", "run", "gunicorn", "-w 4", "-b 0.0.0.0:5000", "app:app"]
