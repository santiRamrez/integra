# Use an official Python runtime as a parent image
FROM python:3.11.0

# Set environment variables
# PYTHONUNBUFFERED ensures console output is not buffered (useful for logs)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app/integra_apis

# Install system dependencies (needed for some python packages usually)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/integra_apis
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

#Manage static files
RUN python manage.py collectstatic --noinput

# Copy project
COPY . /app/

# Collect static files (Ensure you have STATIC_ROOT set in settings.py)
# Note: For production, you usually want WhiteNoise or a GCS bucket.
# RUN python manage.py collectstatic --noinput

# Expose port (Cloud Run expects 8080 by default)
EXPOSE 8080

# Run the application using Gunicorn
# Replace 'myproject.wsgi:application' with your actual project name
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "integra_apis.wsgi:application"]