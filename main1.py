import json
import asyncio
import logging
import logging.config
from fastapi import FastAPI
from fastapi import Request
from fastapi import WebSocket
from fastapi.templating import Jinja2Templates

import folium
import time
import requests
from google.transit import gtfs_realtime_pb2
import json
from kafka import KafkaProducer
from kafka import KafkaConsumer

logger = logging.getLogger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
KAFKA_SERVER = 'localhost:9092'
TOPIC = 'coordinates'

with open('measurements.json', 'r') as file:
    measurements = json.loads(file.read())

consumer = KafkaConsumer(TOPIC,
                             bootstrap_servers=KAFKA_SERVER,
                             api_version=(0, 11, 5),
                             value_deserializer=lambda x: json.loads(x.decode('utf-8')))

stack = []

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        for message in consumer:
            measurements = json.loads(message.value)
            await asyncio.sleep(0.1)
            logger.info(measurements)
            await websocket.send_json(measurements)