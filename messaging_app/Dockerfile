# Use Python 3.10 as the base image
FROM python:3.10

# Prevent Python from writing .pyc files and enable output flushing
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the application code
COPY . /app/

# Expose the port Django runs on
EXPOSE 8000

# Default command to run the Django development server -p
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
