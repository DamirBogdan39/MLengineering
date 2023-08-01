FROM python:3.10.12

# Set working directory inside the container to /app
WORKDIR /app

# Copy the current directory to /app in the container
COPY . .

# Install required libraries and DVC
RUN apt-get update && apt-get install -y cron
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r requirements.txt
RUN pip install --user dvc==3.3.1

# Add /root/.local/bin to the PATH
ENV PATH="/root/.local/bin:${PATH}"