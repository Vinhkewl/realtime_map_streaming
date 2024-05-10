# Realtime_map_tracking

Realtime Maps streaming data platform with Python Kafka 

## Table of Contents
- [Project Description](#project-description)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#test)
- [Disclaimer](#disclaimer)
- [Contributing](#contributing)
- [Future Feature](#future-feature)


## Project Description
In this project we will leverage kafka and gtfs_realtime_pb2 api library to call HSL bus in Norway, track it's longtitude and latitude and display real time on leaflet map library hosted on fast-api server.

On a high level, 3 main component:
- Producer: we need to call the HSL API and then feed it to the producer of kafka 
- Consumer: the consumer will consume the message and open a websocket to reference the location to leaflet map
- HTML: leverage javascript functions and HTML to track realtime the bus locations and display it

## Installation
The required libraries is listed in the requirement.txt

pip install -r requirement.txt

## Usage

I assume that you already know how to hosted a kafka server. If not i have an upcomming post for set up a HA Kafka server here

Step 1: python producer.py

Open another cmd prompt and run
Step 2: python consumer.py

Open web browser and type
Step 3: localhost:8000 


## Test
I have a test notebook for testing code #test1.ipynb

## Contributing
I have listed some of the upcomming feature im going to build for this branch, any recommendations or updates is welcome

## Future Feature
 - GPS shoot coordinate at home server
 - Set up home server with security OAUTH2
 - Design Database so each user can user 1 map
 - Design user and password so they  can log in 
 - Draw line and calculate how many minutes left 

## Disclaimer
- You can actually replace and call any API which includes a latitude and longtitude. However, you will need to adust the schema in core_functions.py

