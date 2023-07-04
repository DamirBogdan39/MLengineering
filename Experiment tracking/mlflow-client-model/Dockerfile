FROM python:3.9

# Set workdir
WORKDIR /mlflow

# Copy data and src
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the server hostname (this should be the service name in the docker-compose file)
ENV MLFLOW_TRACKING_URI=http://mlflow-server:5000/

