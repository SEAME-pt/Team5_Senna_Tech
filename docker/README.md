To build the docker image, do the following command:
```bash
docker build -t <image_name> -f docker/Dockerfile .
```

This add the right context to the build process, so the dockerfile recognizes the car_cluster directory and is able to copy to the container.

To run the docker container opening a terminal, do:
```bash
docker run -it <image_name>
```
