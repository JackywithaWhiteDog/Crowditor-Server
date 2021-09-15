# Crowditor Server

![GitHub last commit](https://img.shields.io/github/last-commit/JackywithaWhiteDog/Crowditor-Server)
![GitHub issues](https://img.shields.io/github/issues/JackywithaWhiteDog/Crowditor-Server)
![GitHub stars](https://img.shields.io/github/stars/JackywithaWhiteDog/Crowditor-Server)
![GitHub license](https://img.shields.io/github/license/JackywithaWhiteDog/Crowditor-Server)

The Flask server with Swagger document for Crowditor API endpoint.

For the frontend interface, check [this repo](https://github.com/Malik705017/Crowditor).

## Table of contents

- [Quick start](#quick-start)
  - [Download data](#download-data)
  - [Manually install dependencies](#manually-install-dependencies)
  - [Run the server](#run-the-server)
  - [Unit test](#unit-test)
  - [Coverage check](#coverage-check)
- [API endpoints](#api-endpoints)
  - [Main endpoints](#main-endpoints)
  - [Helper endpoints](#helper-endpoints)
- [Mock data](#mock-data)
- [Todo](#todo)

## Quick start

The server requires at least `Python 3.8`.

### Download data

Download data from [here](https://drive.google.com/file/d/1gjDPbha6JPJksqgZfR8VhaSw9cHz-oXw/view?usp=sharing), extract it and put the directory at `main/app/data/`.

### Manually install dependencies

Install dependencies using `pip`.

```shell
python -m pip install -r main/requirements.txt
```

### Run the server

Run with default Flask server.

```shell
cd main
python -m flask run
```

Run with Gunicorn server. (not support Windows)

```shell
cd main
python -m gunicorn wsgi:app
```

### Unit test

Using `unittest` library.

```shell
python -m unittest discover -v -s tests/ -p test_*.py
```

### Coverage check

Using `coverage` library

```shell
sh coverage.sh
```

## API endpoints

For the details of api request / response format or status code, check the `/swagger` or `/swagger-ui` endpoints.

### Main endpoints

| Method | Endpoint | Details |
|-|-|-|
| GET | /overview | Requests the overview for crowdfunding projects |
| GET | /advice | Requests the domain-based advice to project editting |
| POST | /estimation | Estimates the performance of the project with modification suggestion |

### Helper endpoints

| Method | Endpoint | Details |
|-|-|-|
| GET | /health | Health check API |
| GET | /swagger | OpenAPI document (JSON format) |
| GET | /swagger-ui | Swagger UI for API endpoint |

## Mock data

For mock data, please check the folder `mock_data`.

## Todo

- [ ] User authorization with `Firebase admin`.
- [ ] Endpoint for listing, getting, adding, updating and deleting project.
