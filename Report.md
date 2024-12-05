# Team 24, Hands-on 9 - Message Brokers

## Short System Description

We created a system that handles text messages with 4 services as separate deployable units. These services are the following:

- API - receives POST request from the users with their message and alias
- Filter - accepts or declines the message based on the absence or presence of stop-words
- Screaming - makes the whole message uppercase
- Publish - sends email to the emails of team members

The system has an event-driven architecture; messages are translated from one service to another one by message brokers (implemented with the use of RabbitMQ). We wrote this system in the Python programming language.

## Load-Testing and Performance Report 

