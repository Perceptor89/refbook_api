# Refbooks
#### Refbooks web API

## Local installation:
You need to clone repository first:
```bash
git clone https://github.com/Perceptor89/refbook_api.git
```

Rename ".env.example" to ".env" and fill it in.

[Install Docker Engine](https://docs.docker.com/engine/install/ubuntu/)

[Docker-compose](https://docs.docker.com/compose/install/standalone/) helps a lot.

You can run app by docker-compose:

```bash
docker-compose up -d --build
```

Load test data from fixture:

```bash
docker exec pkzdrav_backend ./manage.py loaddata /app/refbook/fixtures/data.json
```

By default it starts at http://127.0.0.1:8000/

## Endpoints
Go to http://127.0.0.1:8000/swagger-ui/ to see end points. 

## Technologies used:

| Tool                                                                     | Description                                                                                                           |
|--------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| [Django](https://www.djangoproject.com/)                                 | "The web framework for perfectionists with deadlines."                                                   |
| [Django REST](https://www.django-rest-framework.org)                                 | "Django REST framework is a powerful and flexible toolkit for building Web APIs."                                                   |
| [Git](https://git-scm.com)                                               | Git is a free and open source distributed version control system designed to handle everything from small to very large projects with speed and efficiency.                                                                       |


## Questions and suggestions:
[Telegram](https://t.me/Perceptor89)  
<andreyfominykh@gmail.com>