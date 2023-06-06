# Build the docker image called iris-pytorch-image

docker build -t iris-pytorch-image:1.0.0 .

# Run the docker image to create a container

docker run -it -d --name iris-pytorch-container-1 iris-pytorch-image:1.0.0 /bin/bash

# Open the docker container in an interactive mode

docker exec -it iris-pytorch-container-1 /bin/bash
