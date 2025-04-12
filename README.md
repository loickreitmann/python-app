# Python App

> Example Python App for use with the [From DevOps to Platform Engineering: Master Backstage & IDPs](https://www.udemy.com/course/from-devops-to-platform-engineering-master-backstage-idps/) course created by [Ricardo Andre Gonzalez Gomez](https://www.udemy.com/user/ricardo-andre-gonzalez-gomez/) on Udemy.

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

## Using Helm to Manage Deployment Configuration

Created the charts folder and created our helm app.

```shell
% mkdir charts
% cd charts
% helm create python-app
```

### Install the helm chart on kubernetes

```shell
% cd charts/python-app
% helm install python-app -n python-app . --create-namespace
NAME: python-app
LAST DEPLOYED: Sun Apr  6 14:04:28 2025
NAMESPACE: python-app
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
1. Get the application URL by running these commands:
  http://python-app.local/
```

### Delete the python-app from kubernetes with Helm

```shell
% helm uninstall python-app -n python-app
```

## GitOps: Using Argo CD

### Add the Argo CD Repo to Helm

```shell
% helm repo add argo https://argoproj.github.io/argo-helm
"argo" has been added to your repositories

% helm repo ls
NAME    URL
argo    https://argoproj.github.io/argo-helm
```

### Install Argo CD with Helm

```shell
% cd charts/argocd
% helm upgrade --install argocd argo/argo-cd -n argocd --create-namespace -f values-argo.yaml
Release "argocd" does not exist. Installing it now.
NAME: argocd
STATUS: deployed
REVISION: 1
...
```

## Continuous Deployment with GitHub Actions Self-Hosted Runners

Using an **Actions Runner Controller** (**ARC**) makes it simpler to run self hosted environments on Kubernetes(K8s) cluster.

With ARC you can :

- Deploy self hosted runners on Kubernetes cluster with a simple set of commands.
- Auto scale runners based on demand.
- Setup across GitHub editions including GitHub Enterprise editions and GitHub Enterprise Cloud.

### Prerequisites

We'll use Helm to prepare the installation.

#### Add the JetStack repo

```shell
% helm repo add jetstack https://charts.jetstack.io --force-update
"jetstack" has been added to your repositories
```

#### Install `cert-manager`

```shell
% helm install \
  cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.17.0 \
  --set crds.enabled=true
NAME: cert-manager
LAST DEPLOYED: Sat Apr 12 14:08:13 2025
NAMESPACE: cert-manager
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
cert-manager v1.17.0 has been deployed successfully!
```

### Deploy and Configure ARC

#### Generate a Personal Access Token (PAT) for ARC to authenticate with GitHub

1. Login to your GitHub account and Navigate to "Create new Token."
2. Select repo.
3. Click Generate Token and then copy the token locally ( we’ll need it later).
4. Make a copy the `.env.sample` named `.env`, and past your new token as the value of the `GH_RUNNER_PAT` local environment variable.

#### Add the repository

```shell
% helm repo add actions-runner-controller https://actions-runner-controller.github.io/actions-runner-controller
"actions-runner-controller" has been added to your repositories
```

#### Install Helm chart

```shell
% helm upgrade --install --namespace actions-runner-system --create-namespace\
  --set=authSecret.create=true\
  --set=authSecret.github_token="$GH_RUNNER_PAT"\
  --wait actions-runner-controller actions-runner-controller/actions-runner-controller
```

This will create the `actions-runner-system` namespace. In the next step, we will deploy our runner to that same `actions-runner-system` namespace.

#### Create the GitHub self hosted runners and configure to run against your repository

Create a `runnerdeployment.yaml` file:

```yaml
apiVersion: actions.summerwind.dev/v1alpha1
kind: RunnerDeployment
metadata:
  name: self-hosted-runnerdeploy
spec:
  replicas: 1
  template:
    spec:
      repository: loickreitmann/python-app
```
