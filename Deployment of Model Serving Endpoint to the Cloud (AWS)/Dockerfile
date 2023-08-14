# Use an official Python runtime as a base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file first to leverage Docker's caching
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files to the container's working directory
COPY . .

# Expose port 8000 (the port that FastAPI app will run on)
EXPOSE 8080

# ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

ENTRYPOINT ["python", "main.py"]