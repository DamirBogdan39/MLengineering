# Containerization

This project was created as a part of the homework for EPAMs ML Engineering course. 

In this folder you can see the files and commands used to create a Docker container.

The chosen problem was the to classify the well known Iris data set using neural networks in PyTorch. 

## Creating the image:

To create a a Docker container we must first create the Docker image using the Dockefile file from this folder.

Some of the most notable parts of the Dockerfile are:

`WORKDIR /iris-pytorch` - setting the working directory for which all the next commands will take place.

`RUN pip install -r requirements.txt` - installing all package dependencies used in the project that are defined in the requirements.txt file.

`RUN useradd -u 1000 non-root-user` - adding the new user called non-root-user to demonstrate chaning the user from root to a non-root user.

`USER non-root-user` changing to a non-root user.

To create the image it is necessary to be in the folder which contain the Docker file.

To initiate creating the image the following code was passed to the Linux terminal:

`docker build -t iris-pytorch-image:1.0.0 .`

After the previous code compiles next part of the code creates the container:

`docker run -it -d --name iris-pytorch-container-1 iris-pytorch-image:1.0.0 /bin/bash`

This code creates the container called iris-pytorch-container-1 based on the iris-pytorch-image:1.0.0 image and keeps the container running for the user to work on the dataset/problem.

To open the container in an interactive mode the following part of the code was used:

`docker exec -it iris-pytorch-container-1 /bin/bash`

After the execution of the previous code we are in the bash of the container so we can work from there.

The previous code is contained in the file `script.sh` so to create an image all what is necesarry is to open the terminal in the directory which contains all the files from here and run `./script.sh` which will ensure the creation of image, creating and running the container and opening it in interactive mode.

Working in an interactive mode lets use some of the basic linux commands, for example:

`pwd` which returns `/iris-pytorch` meaning we are in the iris-pytorch directory specified in the Dockerfile.

`whoami` which returns `non-root-user` as specified in the Dockerfile.

`id` which returns `uid=1000(non-root-user) gid=1000(non-root-user) groups=1000(non-root-user)`

## Pulling the already made image:

This image was uploaded to the Docker Hub so it is accessible to pull from Docker Hub using:

`docker pull damirbogdan39/iris-pytorch-image`

After pulling the image the containers can be created in the same way as in the previous example.

## Conclusion

Using the simple iris data set and several python scripts we were able, with the usage of Docker, to create an isolated enviroments with all the dependencies necessary to work on the problem. Giving a tag 1.0.0 to the image insures the correct version control, and setting the user to be a non-root insures the correct permissions are given to use this container. 

