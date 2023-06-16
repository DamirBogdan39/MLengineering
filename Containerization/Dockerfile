FROM python:3.9

# Change working directory

WORKDIR /iris-sklearn

# Specify path to volume

VOLUME /iris-sklearn/data

# Copy everything
    
COPY . . 

# Install requirements

RUN pip install -r requirements.txt

# Add a new user to run docker from 

ARG USER_ID
ARG GROUP_ID

RUN addgroup --gid $GROUP_ID user
RUN adduser --disabled-password --uid $USER_ID --gid $GROUP_ID user

# Set user to user 
USER user

# Run the testing part to get an insight into the classification report

CMD ["python", "test.py"]
