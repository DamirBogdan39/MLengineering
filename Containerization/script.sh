# Build the docker image called iris-pytorch-image

docker build -t iris-sklearn-image:1.0.0 \
    --build-arg USER_ID=$(id -u) \
    --build-arg GROUP_ID=$(id -g) .

# Create a folder with which we will connect the volume and copy all data there

mkdir ~/iris-volume \
    mkdir ~/iris-volume/data \ 
    cp data/*.csv ~/iris-volume/data

# Run the docker image to create a container

docker run -it -d --name iris-sklearn-container-1 \
    -v ~/iris-volume/data:/iris-sklearn/data \
    iris-sklearn-image:1.0.0 /bin/bash

# Open the docker container in an interactive mode

docker exec -it iris-sklearn-container-1 /bin/bash

python test.py