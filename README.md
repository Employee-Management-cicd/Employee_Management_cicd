# Employee Management System – CI/CD

A full-stack Employee Management System built to demonstrate a complete, production-style DevOps pipeline — from code commit to automated testing, containerization, and deployment to Kubernetes.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Run Locally Without Docker](#run-locally-without-docker)
  - [Run with Docker](#run-with-docker)
  - [Run Tests](#run-tests)
- [CI/CD Pipeline](#cicd-pipeline)
- [GitHub Webhook](#github-webhook)
- [Kubernetes Deployment](#kubernetes-deployment)
  - [Kubernetes Scaling](#kubernetes-scaling)
  - [Kubernetes Self-Healing](#kubernetes-self-healing)
- [Docker Compose](#docker-compose)
- [Team and Roles](#team-and-roles)
- [Project Structure](#project-structure)
- [Complete CI/CD Workflow](#complete-cicd-workflow)
- [Project Goals](#project-goals)
- [Benefits of the CI/CD Pipeline](#benefits-of-the-cicd-pipeline)
- [Future Enhancements](#future-enhancements)
- [Conclusion](#conclusion)

---

## Project Overview

<<<<<<< HEAD
This projectttssss is not just a web application; it is a demonstration of real CI/CD (Continuous Integration / Continuous Delivery) pipeline. Every code push is automatically tested, packaged into a Docker container, pushed to Docker Hub, and deployed, with zero manual steps after `git push`.

## Architecture ....
Step 1
=======
This project is not just a web application; it is a demonstration of a real **CI/CD (Continuous Integration / Continuous Delivery)** pipeline.

Every code push is automatically tested, packaged into a Docker container, pushed to Docker Hub, and deployed to Kubernetes with minimal manual intervention.

---

## Architecture

```text
>>>>>>> df1e6be (Updated README file)
Developer's Laptop
        |
        v
   Git Push
        |
        v
 GitHub Repository
        |
        | Webhook
        v
 Jenkins CI/CD Server
        |
        +--> Checkout latest code
        |
        +--> Install dependencies
        |
        +--> Run automated tests
        |
        +--> Build Docker image
        |
        +--> Push image to Docker Hub
        |
        +--> Deploy to Kubernetes
        |
        v
 Running Application
```

---

## Tech Stack

| Layer               | Technology            |
|---------------------|-----------------------|
| Application         | Python + Flask        |
| Database            | SQLite + SQLAlchemy   |
| Testing             | pytest, pytest-flask  |
| Containerization    | Docker                |
| Orchestration       | Kubernetes (Kind)     |
| CI/CD               | Jenkins               |
| Pipeline Automation | Jenkins Pipeline      |
| Container Registry  | Docker Hub            |
| Version Control     | Git + GitHub          |
| Webhook             | GitHub Webhook        |

---

## Features

- Add employees
- View employees
- Edit employee details
- Delete employees
- Search employees
- Duplicate email validation
- Automated test suite
- Automated CI/CD pipeline
- GitHub webhook integration
- Automatic Docker image build
- Automatic Docker Hub push
- Automatic Kubernetes deployment
- Kubernetes horizontal scaling
- Kubernetes self-healing

---

## Getting Started

### Prerequisites

Install the following tools:

- Python 3.11 or later
- Docker Desktop
- Git
- Kubernetes
- Kind
- kubectl
- Jenkins

### Run Locally Without Docker

**1. Clone the Repository**

```bash
git clone <your-github-repository-url>
cd Employee_Management_cicd
```

**2. Install Dependencies**

```bash
pip install -r requirements.txt
```

**3. Run the Application**

```bash
python run.py
```

**4. Open the Application**

Open the following URL in your browser:

```text
http://localhost:5000
```

### Run with Docker

**1. Build the Docker Image**

```bash
docker build -t employee-management .
```

**2. Run the Container**

```bash
docker run -d -p 5000:5000 employee-management
```

**3. Open the Application**

```text
http://localhost:5000
```

### Run Tests

Run the automated test suite using:

```bash
pytest tests/
```

The test suite verifies the core functionality of the application.

> **Note:** If any test fails during the Jenkins pipeline, the pipeline stops and the later stages are not executed.

---

## CI/CD Pipeline

The `Jenkinsfile` defines the CI/CD pipeline for the project. The pipeline contains the following stages:

### 1. Checkout

Jenkins pulls the latest source code from the GitHub repository.

### 2. Install Dependencies

Jenkins installs all required Python packages from `requirements.txt`.

### 3. Run Tests

Jenkins runs the automated test suite:

```bash
pytest tests/
```

If any test fails, the pipeline stops at this stage.

### 4. Build Docker Image

After successful testing, Jenkins builds a Docker image containing the application.

### 5. Push Image to Docker Hub

The Docker image is pushed to Docker Hub so that it can be used for deployment.

### 6. Deploy

The application is deployed to Kubernetes using the Kubernetes configuration files.

---

## GitHub Webhook

The pipeline is designed to trigger automatically whenever new code is pushed to GitHub.

```text
Code Push
    |
    v
GitHub
    |
    | Webhook
    v
Jenkins
    |
    v
Checkout Code
    |
    v
Install Dependencies
    |
    v
Run Tests
    |
    v
Build Docker Image
    |
    v
Push Image to Docker Hub
    |
    v
Deploy to Kubernetes
```

This removes the need to manually start a Jenkins build after every GitHub push.

### Local Jenkins Webhook

If Jenkins is running locally on `localhost`, GitHub cannot directly access the local Jenkins server.

A tunneling service such as **ngrok** can be used to create a temporary public URL for the Jenkins webhook. This allows GitHub to send webhook requests to the locally running Jenkins server.

---

## Kubernetes Deployment

The `k8s/` directory contains the Kubernetes configuration files:

```text
k8s/
├── deployment.yaml
└── service.yaml
```

### Deployment

The `deployment.yaml` file defines how the application should run in Kubernetes. The deployment can run multiple replicas of the application.

### Service

The `service.yaml` file exposes the application through a Kubernetes service.

### Apply Kubernetes Configuration

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### Check Kubernetes Resources

```bash
# Check the deployments
kubectl get deployments

# Check the pods
kubectl get pods

# Check the services
kubectl get services
```

### Access the Application Using Port Forwarding

```bash
kubectl port-forward service/employee-management-service 7000:5000
```

Then open:

```text
http://localhost:7000
```

### Kubernetes Scaling

Kubernetes allows the application to run multiple replicas. For example, scale the deployment to five replicas:

```bash
kubectl scale deployment employee-management --replicas=5
```

Check the running pods:

```bash
kubectl get pods
```

This allows multiple instances of the application to run simultaneously.

### Kubernetes Self-Healing

Kubernetes maintains the desired number of replicas. If a running pod crashes or is deleted, Kubernetes automatically creates a replacement pod.

```text
Desired replicas: 2

Pod 1
Pod 2

       |
       | Pod 1 crashes
       v

Pod 2
New Pod
```

This provides basic fault recovery and improves application availability.

---

## Docker Compose

The project also contains a `docker-compose.yml` file for running the application using Docker Compose.

Start the application:

```bash
docker compose up --build
```

Stop the containers:

```bash
docker compose down
```

---

## Team and Roles

| Member   | Role                        | Responsibilities                                                  |
|----------|-----------------------------|-------------------------------------------------------------------|
| Member 1 | Application Developer       | Flask application, database, CRUD functionality and tests         |
| Member 2 | Docker Engineer             | Dockerfile, Docker containers and Docker Hub                      |
| Member 3 | CI/CD & Kubernetes Engineer | Jenkins pipeline, GitHub integration and Kubernetes deployment    |

---

## Project Structure

```text
Employee_Management_cicd/
<<<<<<< HEAD
├── app/                    Flask application
├── tests/                  Automated test suite
├── k8s/                    Kubernetes deployment and service configs
├── Dockerfile              Container build instructions
├── docker-compose.yml      Multi-container orchestration
├── Jenkinsfile             CI/CD pipeline definition
├── requirements.txt        Python dependencies
└── run.py                  Application entry point
# Last updated: webhook test
# retry
## retry
# webhook retest
# clean webhook test
# retest after jenkins restart
# test after job recreation
# test after manual build 1 completed
# direct build list test
# retest after jenkins restart
=======
│
├── app/
│   └── Flask application
│
├── tests/
│   └── Automated test suite
│
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
│
├── Dockerfile
├── docker-compose.yml
├── Jenkinsfile
├── requirements.txt
├── run.py
└── README.md
```

---

## Complete CI/CD Workflow

```text
Developer
    |
    | Git Push
    v
GitHub Repository
    |
    | GitHub Webhook
    v
Jenkins
    |
    +-----------------------+
    |                       |
    v                       |
Checkout Code               |
    |                       |
    v                       |
Install Dependencies        |
    |                       |
    v                       |
Run Automated Tests         |
    |                       |
    v                       |
Build Docker Image          |
    |                       |
    v                       |
Push Image to Docker Hub    |
    |                       |
    v                       |
Deploy to Kubernetes <------+
    |
    v
Running Application
```

---

## Project Goals

The main goal of this project is to demonstrate how a modern DevOps workflow can automate the software delivery process.

The project demonstrates:

- Continuous Integration
- Continuous Delivery
- Automated Testing
- Docker Containerization
- Docker Image Management
- Jenkins Pipeline Automation
- GitHub Webhook Integration
- Kubernetes Deployment
- Horizontal Scaling
- Self-Healing
- Version Control

---

## Benefits of the CI/CD Pipeline

| Benefit                | Description                                                                    |
|------------------------|--------------------------------------------------------------------------------|
| Faster Development     | Automated testing and deployment reduce the time required to release changes.  |
| Fewer Manual Errors    | The pipeline performs repetitive deployment tasks automatically.               |
| Consistent Deployments | Docker provides a consistent application environment across different systems. |
| Automated Testing      | Every code change is tested before deployment.                                 |
| Scalability            | Kubernetes allows the application to run multiple replicas.                    |
| Self-Healing           | Kubernetes automatically replaces failed application pods.                     |

---

## Future Enhancements

- Add user authentication and authorization
- Replace SQLite with PostgreSQL or MySQL
- Add Kubernetes Ingress
- Add HTTPS/TLS
- Add Prometheus monitoring
- Add Grafana dashboards
- Add centralized logging
- Add automated rollback
- Add Kubernetes Horizontal Pod Autoscaler
- Deploy the application to a cloud platform
- Add security scanning to the CI/CD pipeline

---

## Conclusion

The Employee Management System demonstrates a complete DevOps lifecycle.

A developer pushes code to GitHub, which triggers Jenkins through a GitHub webhook. Jenkins then checks out the code, installs dependencies, runs automated tests, builds a Docker image, pushes the image to Docker Hub, and deploys the application to Kubernetes.

This project shows how **CI/CD, Docker, Jenkins, GitHub, and Kubernetes** work together to create an automated and reliable software delivery pipeline.
>>>>>>> df1e6be (Updated README file)
