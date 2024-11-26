# Project implementing Event Driven Architecture Pattern

## Project demo

It can be viewed on YouTube: <https://youtu.be/AJVNYYS_Fjg>

## Project structure

```txt
.
├── Dockerfile  # build the project for Docker
├── README.md  # you are reading this file :)
├── docker-compose.yml  # launching RabbitMQ and servies in Docker containers
├── requirements.txt  # used external packages
└── src  # where the source code lies
    ├── config.py  # various settings for, e.g., RabbitMQ and SMTP
    ├── schemas.py  # Pydantic model for Message
    └── services  # each service is in a separate folder
        ├── api
        │   └── service.py   # service.py gets launched from each folder
        ├── filter
        │   ├── blacklist.txt  # blacklisted words
        │   └── service.py
        ├── publish
        │   └── service.py
        └── screaming
            └── service.py
```

## Usage

1. Fill out `.env` file based on the provided example file `.env.sample`
2. Run RabbitMQ: `docker compose up --build -d rabbitmq`
3. When RabbitMQ starts, run the services: `docker compose up --build -d api filter screaming publish`
4. Open Swagger IU at <http://localhost:8932/docs>

## Team members

Team 24:

- Gleb Bugaev ([g.bugaev@innopolis.university](mailto:g.bugaev@innopolis.university))
- Nail Minnemullin ([n.minnemullin@innopolis.university](mailto:n.minnemullin@innopolis.university))
- Dmitriy Okoneshnikov ([d.okoneshnikov@innopolis.university](mailto:d.okoneshnikov@innopolis.university))
- Vladislav Bolshakov ([v.bolshakov@innopolis.university](mailto:v.bolshakov@innopolis.university))
