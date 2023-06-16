# Containerization

This project was created as a part of the homework for EPAMs ML Engineering course. 

In this folder you can see the files and commands used to create a Docker container.

The chosen problem was the to classify the well known Iris data set using a Decision Tree Classifier from sci-kit learn. 

## Creating the image:

To create a a Docker container we must first create the Docker image using the Dockefile file from this folder.

Some of the most notable parts of the Dockerfile are:

`WORKDIR /iris-sklearn` - setting the working directory for which all the next commands will take place.

`VOLUME /iris-sklearn/data` - the data folder in the workdir is defined as the volume with which we will connect out host machine to share data.

`RUN pip install -r requirements.txt` - installing all package dependencies used in the project that are defined in the requirements.txt file.

`ARG USER_ID` - accept an argument called USED_ID

`ARG GROUP_ID` - accept an argument called GROUP_ID

`RUN addgroup --gid $GROUP_ID user` - add the group with the GROUP_ID argument

`RUN adduser --disabled-password --uid $USER_ID --gid $GROUP_ID user` - Add the user with USER_ID and and add it to the group.

`USER user` - set `user` as user

To create the image it is necessary to be in the folder which contain the Docker file.

To initiate creating the image the following code was passed to the Linux terminal:

``` bash
docker build -t iris-sklearn-image:1.0.0 \
    --build-arg USER_ID=$(id -u) \
    --build-arg GROUP_ID=$(id -g) .
```
The next part of the code does the following:
1. create a directory on the machines home path called iris-volume/data
2. copies the necessary data to the directory so it can be linked via volume

```bash
mkdir ~/iris-volume \
    mkdir ~/iris-volume/data \ 
    cp data/*.csv ~/iris-volume/data
```
After the previous code compiles next part of the code creates the container:

``` bash
docker run -it -d --name iris-sklearn-container-1 \
    -v ~/iris-volume/data:/iris-sklearn/data \
    iris-sklearn-image:1.0.0 /bin/bash
```

This code creates the container called iris-sklearn-container-1 based on the iris-sklearn-image:1.0.0 image and keeps the container running for the user to work on the dataset/problem. This command also linked the ~/iris-volume/data to the /iris-sklearn/data from the container so we can work with he necessary .csv files. This assures us that we work from the container but all changes made to the data will be saved on out machine. The folder path and name `/iris-sklearn/data` is arbitrary and can be modified by the user of the container if the user prefers to store the data somewhere else.

To open the container in an interactive mode the following part of the code was used:

```bash
docker exec -it iris-sklearn-container-1 /bin/bash
```

After the execution of the previous code we are in the bash of the container so we can work from there.

The previous code is contained in the file `script.sh` so to create an image all what is necesarry is to open the terminal in the directory which contains all the files from here and run `./script.sh` which will ensure the creation of image, creating and running the container and opening it in interactive mode.

Working in an interactive mode lets use some of the basic linux commands, for example:

```bash
pwd
```
which returns:

```bash
/iris-sklearn
```
meaning we are in the iris-pytorch directory specified in the Dockerfile.

```bash
whoami
``` 
which returns:

```bash
user
```
as specified in the Dockerfile.

```bash
id
```
which returns:

```bash
uid=1000(user) gid=1000(user) groups=1000(user),100(users)
```
This return could possibly vary from machine to machine on which the container is running because it takes the arguments when the image is being built.

Finally, let's try running the `test.py` script which should return us back the classification report of the iris classification:
```bash
python test.py
```
if everything is working correctly it will output:
```bash
             precision    recall  f1-score   support

         0.0       1.00      1.00      1.00        29
         1.0       0.83      0.87      0.85        23
         2.0       0.86      0.83      0.84        23

    accuracy                           0.91        75
   macro avg       0.90      0.90      0.90        75
weighted avg       0.91      0.91      0.91        75
```
## Pushing the image to Docker Hub:
The three following command explain how to push an already made image to the Docker Hub.

1. We must tag the image:

```bash
docker tag iris-sklearn-image:1.0.0 damirbogdan39/iris-sklearn-image:1.0.0
```

2. Next up is logging into docker:

```bash
docker login
```

3. Lastly, we push the image with the `push`:

```bash
docker push damirbogdan39/iris-sklearn-image:1.0.0
```
## Pulling the already made image:

This image was uploaded to the Docker Hub so it is accessible to pull from Docker Hub using:

```bash
docker pull damirbogdan39/iris-sklearn-image:1.0.0
```

After pulling the image the containers can be created in the same way as in the previous example.

### Important

This is not reccomended to pull the image because when in the moment of building the image the `USER_ID` and `GROUP_ID` were taken as arguments from the device that built the image and could make some permission problems. This part is to demonstrate how it is possible to push the image on Docker Hub and pull it later on.

For everything to be set up correctly it is reccomended to pull this repository and run the `./script.sh`.

## Conclusion

Using the simple iris data set and several python scripts we were able, with the usage of Docker, to create an isolated enviroments with all the dependencies necessary to work on the problem. Giving a tag 1.0.0 to the image insures the correct version control, and setting the user to be a non-root insures the correct permissions are given to use this container. 
