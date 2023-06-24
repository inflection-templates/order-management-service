## Build and Run Docker Image
1. Create new file in root directory of application. Name it `Dockerfile`.

2. Write configurations as given in this [file](../Dockerfile).

3. Save the file. Open terminal and run command:
    ```
    docker build -t order-service .
    ```
    This will build a docker image named `order-service` from Dockerfile. It may take few minutes to finish the process.
&nbsp;<br>
4. Once finished, verify the image you built. To do so, run following command in terminal:
    ```
    docker images
    ```
    This will list out all docker images you have so far. Check whether `order-service` is there in the list.
&nbsp;<br>

5. To run docker container using this image, run command:
    ```
    docker run -d -p 12345:12345 --name order-container order-service
    ```
6. To see the running containes, execute following command:
    ```
    docker ps
    ```
    You may see your `order-container` there.

7. To test application, go to browser and browse for `http://localhost:12345`. You may see a message like `Order-Management-Service is running on port 12345`. You may now test api routes for various models using `Postman`.
&nbsp;<br>
8. To stop container, use command:
    ```
    docker stop order-container
    ```
    To remove container, run command:
    ```
    docker rm order-container
    ```

## Docker Compose

To test whole application in containerized environment, you need to use `Docker-compose`. We need three containers i.e. database-container, application-container and either Zipkin or Jaeger container. So instead of running them separately, we can run them in one go using `Docker-compose`. To do so, follow these steps:
1. Create a new file in root directory of application and name it `docker-compose.yml`.
2. Write configurations for three containers in `Yaml` format. Refer this [file](../docker-compose.yml).
3. Once finished with configurations, save the file and open terminal. Run following command:
    ```
    docker compose up --build -d
    ```
    This command will pull docker images for `MYSQL` and `Zipkin` from docker hub and use them to run their containers and it will also build docker image of application using `Dockerfile` that we have already created.

4. To see list of running containers, run command:
    ```
    docker compose ps
    ```

5. Now you may access application at `http://localhost:12345` and Zipkin UI at `http://localhost:9411`. Test application by sending `Postman` requests. You may see thr traces of your requests on Zipkin UI.

6. To stop and remove all containers, run command:
    ```
    docker compose down
    ```