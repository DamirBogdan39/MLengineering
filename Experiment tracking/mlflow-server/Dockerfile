FROM python:3.9

# Set workdir
WORKDIR /mlflow

# Copy content for server
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt