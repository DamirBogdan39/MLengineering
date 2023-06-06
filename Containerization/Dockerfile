FROM ubuntu:latest

# Install python and pip

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip



# Change working directory

WORKDIR /iris-pytorch

# Copy everything
    
COPY . . 

# Install requirements

RUN pip install -r requirements.txt

# Add a new user to run docker from 

RUN useradd -u 1000 non-root-user 

# Change to non-root priviledge user

USER non-root-user

# Run the test part of the neural network

CMD ["python3", "test.py"]
