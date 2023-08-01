docker build -t batch_serving_image .

docker run -it -d --name batch_serving_container-1 \
    -v ./data:/app/data \
    -v ./cron_logs:/app/cron_logs \
    batch_serving_image /bin/bash


docker exec -it batch_serving_container-1 /bin/bash