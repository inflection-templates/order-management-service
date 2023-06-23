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

