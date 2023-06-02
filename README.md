# Sabkino backend project
Sabkino is an online clothes shop website for both customers and sellers. This project is the implementation of the backend part of this website.

## Table of content
* [Analysis](#analysis)
* [API Implementation](#api-implementation)
* [Tests](##tests)
* [Logging APIs](#logging-apis)
* [Dockerization](#dockerization)

## Analysis
### Define Recuirements
[The link of Sabkino's requirements](https://docs.google.com/document/d/15xuDdvQncoIcrMqIQ0CIrqrO8BVc2PzDm2mepGpAEnQ/edit?usp=sharing)

### Usecase Diagrams
First, all the usecases were extracted from the requirements, and then, related diagrams were drawn.
[The link of the usecase diagrams]()

### Write Scenarios
[The link of Sabkino's scenarios](https://docs.google.com/document/d/1AEV4EWQozmOpbjI8UFH5tvYHM67fCUc_6IZIAeQJ6NA/edit?usp=sharing)

### Sequence Diagrams
The sequence diagrams were drawn based on the scenarios.
[The link of the sequence diagrams]()

### Class Diagram
The class diagram was drawn based on the sequence diagrams and the requirements.
[The link of the class diagram]()

### System's Architecture
The module based architecture was chosen for this system.
[The link of the diagram and its descriptions](https://docs.google.com/document/d/1-iI7lRHndX9pLfUV0vwTH-IEA7BxyDL47pLU6yHSdGI/edit?usp=sharing)

## API Implementation
Django Rest Framework was used to write the apis. The project includes following apps:

* accounts
* products
* shoppingCarts
* favoriteProducts
* wallets
* gifts
* orders

### How To Run The Project
To run the project first install all the libraries which have been witten in the [requirements file](https://github.com/ashrafizahra81/SE-Prj-Backend/blob/main/requirements.txt). Then, use "py manage.py runserver" command in the terminal.

## Tests
144 tests were written for all the apps, with 99% of coverage. 

### CI/CD
[![Django CI](https://github.com/ashrafizahra81/SE-Prj-Backend/actions/workflows/django.yml/badge.svg)](https://github.com/ashrafizahra81/SE-Prj-Backend/actions/workflows/django.yml)

## Logging APIs
All the apis were logged, and the results were saved in two files called INFO.log and ERROR.log.

## Dockerization
A [dockerfile](https://github.com/ashrafizahra81/SE-Prj-Backend/blob/main/Dockerfile) was written for the project, and an image and a container were created. Then the project was dockerized.

### How to Run
To run the container of this project, first use "docker pull zarashrafi/drf-app" command. Then run the container with "docker run -d -p 8080:8000 zarashrafi/drf-app" command.









































