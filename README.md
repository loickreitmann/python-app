# Python App

## Setup

You'll need Devbox installed, and the ideal IDE is Visual Studio Code.

### Install the Python dependencies

```shell
> devbox shell
> pip install -r requirements.txt
```

## Running in development mode

```shell
> flask --app app.py --debug run
 * Serving Flask app 'app.py'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
 ```

## Building the image

```shell
> docker build -t python-app:v2 .
```

## Running the image in Docker

> Note: You'll need Docker Desktop locally.

```shell
> docker run -p 8080:5000 python-app:v2
```

## Tag and Push Image to Docker Hub

> Note: You'll need to have a Docker Hub account and to have you local environment set up to authenticare with Docker Hub using an access token.

```shell
> docker tag python-app:v2 loickreitmann/python-app:v2
> docker push loickreitmann/python-app:v2
```
