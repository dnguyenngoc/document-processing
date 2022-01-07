# Document Processing
[![Python](https://img.shields.io/badge/python-3.9.5-green)](https://www.python.org/downloads/release/python-395/)
[![NPM](https://img.shields.io/badge/npm-1.0.1-green)](https://www.npmjs.com/package/package/v/1.0.1)
[![Celery](https://img.shields.io/badge/celery-5.1.2-orange)](https://docs.celeryproject.org/en/stable/getting-started/introduction.html)
[![Redis](https://img.shields.io/badge/redis-6.2.6-orange)](https://redis.io/)
[![Rabitmq](https://img.shields.io/badge/rabbitmq-3.9.11-pink)](https://www.rabbitmq.com/)
[![Posgresql](https://img.shields.io/badge/postgres-14.1-brown)](https://www.postgresql.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.63-lightgrey)](https://fastapi.tiangolo.com/)
[![Tensorflow](https://img.shields.io/badge/tensorflow-3.7-yellowgreen)](https://analyticsindiamag.com/tensorflow-2-7-0-released-all-major-updates-features/)
[![Pytorch](https://img.shields.io/badge/pytorch-1.10-blue)](https://pytorch.org/blog/pytorch-1.10-released/)

This is project how to build full workflow ocr processing for mutiple document type (static form, free-form, bank-form ...). In the first release we try to make full system with cloud service. And the second release we will try to build all system on cluster raspberry pi with k8s. New release is comming :fire: :fire: :fire: :fire:

## Screenshots & Gifs

**View System**

<div>
    <kbd>
        <img title="View System" src="https://github.com/apot-group/document-processing/blob/main/o-statics/images/server.png?raw=true" />
    </kbd>
    <br/>
</div>
<br>

**Gallery**
<div>
    <kbd>
        <img title="View System" src="https://github.com/apot-group/document-processing/blob/main/o-statics/images/demo.png?raw=true" />
    </kbd>
    <br/>
</div>
<br>

## Contents
- [Screenshots & Gifs](#screenshots--gifs)
- [App API](https://github.com/apot-group/document-processing/blob/master/dp_api/README.md#api-documents)
   - [Why FastAPI?](https://github.com/apot-group/document-processing/blob/master/dp_api/README.md#why-fastapi)
   - [Why Celery?](https://github.com/apot-group/document-processing/blob/master/dp_api/README.md#why-celery)
   - [API documents](https://github.com/apot-group/document-processing/blob/master/dp_api/README.md#api-documents-1)
      - [1. Login Accept Token](https://github.com/apot-group/document-processing/blob/master/dp_api/README.md#1-login-accept-token)
      - [2. Login Refresh Token](https://github.com/apot-group/document-processing/blob/master/dp_api/README.md#2-login-refresh-token)
      - [3. ML Predict](https://github.com/apot-group/document-processing/blob/master/dp_api/README.md#3-ml-predict)
      - [4. ML Status](https://github.com/apot-group/document-processing/blob/master/dp_api/README.md#4-ml-status)
- [App Paragraph](https://github.com/apot-group/document-processing/blob/master/dp_paragraph/README.md#app-paragraph)
- [App Field](https://github.com/apot-group/document-processing/blob/master/dp_field/README.md#app-field)
- [App OCR](https://github.com/apot-group/document-processing/blob/master/dp_ocr/README.md#app-ocr)
- [For developer](#for-dev)
- [Contact Us](#contact-us)

<!-- ## Structure
We will try more Machine learing/Deep learning to processing Image(document-processing) in future. Now will just focus on how to make full system work well on pi4 clustering with kuberneter. :fire: :fire: :fire:.
```
├── web-service
│   └── dp-client // react
├── api-service
│   └── dp-api // golang gin/gorm
├── ml-service
│   ├──pre-processing 
│       └── dp-idcard-preprocesing // python celery
│   ├──field-processing 
│       └── dp-idcard-field-detection // python celery
│   ├──ocr-engine 
│       └── dp-vietnamese-ocr // python celery
├── other-service
    └── dp-database // postgres
    └── dp-redis // redis
    └── dp-rabitmq // rabbitmq
```
- **Link Component for more details**: -->
<!-- 
    - **Client** -  https://github.com/apot-group/document-processing/blob/main/dp-client/README.md

    - **Api** -  https://github.com/apot-group/document-processing/blob/main/dp-api/README.md
    
    - **Id Card Pre Processing** - https://github.com/apot-group/document-processing/blob/main/dp-idcard-preprocessing/README.md
    
    - **Id Card Field Processing** - https://github.com/apot-group/document-processing/blob/main/dp-idcard-field-detection/README.md
        
    - **Vietnamese Ocr** - https://github.com/apot-group/document-processing/blob/main/dp-vietnameese-ocr/README.md -->


## For Dev

### 1. Install docker and docker-compose:

`https://www.docker.com/`

### 2. Copy config file to /app/env-stag.ini
`contact with admin of project to get this file` 

### 3. From project dir:

`docker-compose up`

### 4. Api Docs

Api docs at: http://localhost/api/docs#/ or http://localhost/api/redoc#/

### 5. Frontend

Frontend at http://localhost

## Contact Us

- Email-1: duynnguyenngoc@hotmail.com - Duy Nguyen :heart: :heart: :heart: 
- Email-2: ngocnghia128@gmail.com - Nghia Nguyen - :fire: :fire: :fire: 
