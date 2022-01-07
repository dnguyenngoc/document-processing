# Api documents
We provide extract API which provide cropped paragraphs and fields of Ancestry document for DGS3.
We using FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints. And Using Celery Task queues like message transport to send and receive messages. :fire: :fire: :fire:.

## Contents
- [Why FastApi?](#why-fastapi)
- [Why Celery?](#why-celery)
- [API documents](#api-documents-1)
   - [1. Login Accept Token](#1-login-accept-token)
   - [2. Login Refresh Token](#2-login-refresh-token)
   - [3. ML Predict](#3-ml-predict)
   - [4. ML Status](#4-ml-status)
- [Contact Us](#contact-us)

## Why FastApi?

- **Fast**: Very high performance, on par with NodeJS and Go (thanks to Starlette and Pydantic). One of the fastest Python frameworks available.

- **Fast to code**: Increase the speed to develop features by about 200% to 300%. *

- **Fewer bugs**: Reduce about 40% of human (developer) induced errors. *
Intuitive: Great editor support. Completion everywhere. Less time debugging.
- **Easy**: Designed to be easy to use and learn. Less time reading docs.
- **Short**: Minimize code duplication. Multiple features from each parameter declaration. Fewer bugs.
- **Robust**: Get production-ready code. With automatic interactive documentation.
- **Standards-based**: Based on (and fully compatible with) the open standards for APIs: OpenAPI (previously known as Swagger) and JSON Schema.

## Why Celery?
- **Simple**: Celery is easy to use and maintain, and it doesn’t need configuration files. It has an active, friendly community you can talk to for support, including a mailing-list and an IRC channel. Here’s one of the simplest applications you can make:
    ```python
        from celery import Celery

        app = Celery('hello', broker='amqp://guest@localhost//')

        @app.task
        def hello():
            return 'hello world'
    ```
- **Highly Available:** Workers and clients will automatically retry in the event of connection loss or failure, and some brokers support HA in way of Primary/Primary or Primary/Replica replication.

- **Fast:** A single Celery process can process millions of tasks a minute, with sub-millisecond round-trip latency (using RabbitMQ, librabbitmq, and optimized settings).

- **Flexible:** Almost every part of Celery can be extended or used on its own, Custom pool implementations, serializers, compression schemes, logging, schedulers, consumers, producers, broker transports, and much more.


## API Documents
All API requests require the use of a generated basic auth. You can create basic auth, or generate a new one, by POST user/pass to login-acces-token url.

### 1. Login Accept Token
- **Request:**
```http
POST /api/v1/account/login/access-token
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `username` | `string` | **Required**.|
| `password` | `string` | **Required**.|

- **Response:**
```yaml
{
  "token_type": "bearer",
  "access_token": "72dbec042d78266a882683fafb7e503798f4fdf0e52d97120785672...",
  "refresh_token": "84a28abf73dde156aff9f34e4bece9351d0cda750a7549ac4f29a3...",
  "expire_token": "2022-01-04T10:46:08.511665",
  "expire_refresh_token": "2022-01-04T11:16:08.512254"
}
```

### 2. Login Refresh Token
```http
POST /api/v1/account/login/refresh-token
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `refresh_token` | `string` | **Required**.|

- **Response:**
```yaml
{
  "token_type": "bearer",
  "access_token": "72dbec042d78266a882683fafb7e503798f4fdf0e52d97120785672...",
  "refresh_token": "84a28abf73dde156aff9f34e4bece9351d0cda750a7549ac4f29a3...",
  "expire_token": "2022-01-04T10:46:08.511665",
  "expire_refresh_token": "2022-01-04T11:16:08.512254"
}
```
### 3. ML Predict
```http
POST api/v1/ml/process/
```
<!-- |AUTHORIZATIONS:| **required**.| -->
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `file` | `binary` | **Required**.|
| `@Authorizations` | `bearer` | **Required**.|


### 4. ML Status
```http
GET api/v1/ml/status/{task_id}
```
<!-- |AUTHORIZATIONS:| **required**.| -->
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `task_id` | `string` | **Required**.|
| `@Authorizations` | `bearer` | **Required**.|

- **Response:**
```yaml
{
  "task_id": "c0c3d0f4-5361-5b17-8717-97663e01d66c",
  "status": {
    "general_status": "SUCCESS",
    "upload_status": "SUCCESS",
    "paragraph_status": "SUCCESS",
    "field_status": "SUCCESS"
  },
  "time": {
    "start_upload": "1641274802.993376",
    "end_upload": "1641274803.733474",
    "start_paragraph": "1641274804.106201",
    "end_paragraph": "1641274814.693461",
    "start_field": "1641274815.546758",
    "end_field": "1641274857.970672"
  },
  "upload_result": {
    "path": "./storages/ml/upload/2022-01-04/c0c3d0f4-5361-5b17-8717-97663e01d66c.JPEG",
    "file_type": ".JPEG"
  },
  "paragraph_result": {
    "paragraph_0": {
      "confidence_level": "1.0",
      "box": "1490,74,2971,1345"
    },
    ...
  },
  "field_result": {
    "paragraph_0": {
      "content_birth_day": {
        "boxes": [
          "1562,814,1623,1139",
          "1571,954,1628,1048"
        ],
        "confidence_level": "0.28"
      },
      "content_birth_year": {
        "boxes": [
          "1569,508,1620,810"
        ],
        "confidence_level": "0.61"
      },
      ...
    }
    ...
    }
  },
  "error": null
}
```
