# Python App

## Setup

You'll need Devbox installed, and the ideal IDE is Visual Studio Code.

### Install the Python dependencies

```shell
% devbox shell
% pip install -r requirements.txt
```

## Running in development mode

```shell
% flask --app app.py --debug run
 * Serving Flask app 'app.py'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
 ```

## Running Locally in Docker

> Note: You'll need Docker Desktop locally.

### Building the image

```shell
% docker build -t python-app:v2 .
```

### Running the image in Docker

```shell
% docker run -p 8080:5000 python-app:v2
```

### Tag and push image to Docker Hub

> Note: You'll need to have a Docker Hub account and to have you local environment set up to authenticare with Docker Hub using an access token.

```shell
% docker tag python-app:v2 loickreitmann/python-app:v2
% docker push loickreitmann/python-app:v2
```

## Running Locally Kubernetes

> Note: You'll need Rancher Desktop running locally.

### Apply the K8s configurations to run in Kubernetes

```shell
% kubectl apply -f k8s/deploy.yaml
% kubectl apply -f k8s/service.yaml
% kubectl apply -f k8s/ingresss.yaml
```

### Take a look a how things running

```shell
% kubectl describe svc python-app
Name:                     python-app
Namespace:                default
Labels:                   <none>
Annotations:              <none>
Selector:                 app=python-app
Type:                     ClusterIP
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       10.43.47.207
IPs:                      10.43.47.207
Port:                     <unset>  8080/TCP
TargetPort:               5000/TCP
Endpoints:                10.42.0.239:5000
Session Affinity:         None
Internal Traffic Policy:  Cluster
Events:                   <none>
```

```shell
% kubectl get ing
NAME         CLASS     HOSTS              ADDRESS      PORTS   AGE
python-app   traefik   python-app.local   10.0.0.206   80      5m23s
```

### Deleting the deployments

```shell
% kubectl delete -f k8s
deployment.apps "python-app" deleted
ingress.networking.k8s.io "python-app" deleted
service "python-app" deleted
```
