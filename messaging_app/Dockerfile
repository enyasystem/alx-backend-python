# Use official Python base image
FROM python:3.10

# Set work directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# Expose the port Django runs on
EXPOSE 8000

# Run migrations and start the server with -p option
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver -p 8000 0.0.0.0:8000"]
