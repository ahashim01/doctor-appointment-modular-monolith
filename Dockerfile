# Use a lightweight Python 3.10 image
FROM python:3.12-slim

# Set a working directory inside the container
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the default Django port
EXPOSE 8000

# The command to run when the container starts:
# 1. Run migrations (using SQLite)
# 2. Start the dev server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
