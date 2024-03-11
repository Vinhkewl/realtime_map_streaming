import json
import folium
import time
import re
import requests
from google.transit import gtfs_realtime_pb2
from json import dumps
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaConsumer

try:
    admin_client = KafkaAdminClient(
        bootstrap_servers="localhost:9092",
        client_id='tracking'
    )

    topic_list = [NewTopic(name="coordinates", num_partitions=1, replication_factor=1)]
    admin_client.create_topics(new_topics=topic_list, validate_only=False)
except:
    pass

api_url = 'https://realtime.hsl.fi/realtime/vehicle-positions/v2/hsl'  # Replace with your API endpoint
KAFKA_SERVER = 'localhost:9092'
TOPIC = 'coordinates'


def fetch_coordinates():
    response = requests.get(api_url)
    if response.status_code == 200:
        # Fetch the GTFS-RT payload
        response = requests.get(api_url)
        payload = response.content

        # Create a GTFS-RT feed message
        feed = gtfs_realtime_pb2.FeedMessage()

        # Parse and decode the payload
        feed.ParseFromString(payload)

        # Create a list to hold the decoded entities
        decoded_entities = []

        # Iterate over the feed entities
        for entity in feed.entity:
            # Convert the entity to a dictionary
            # 18/165 47/668 22/943 22/945 22/944
            if re.search(r'22/944', entity.id):
                entity_dict = {
                    'id': entity.id,
                    'vehicle': {
                        'trip': {
                            'route_id': entity.vehicle.trip.route_id,
                            'start_time': entity.vehicle.trip.start_time,
                            'start_date': entity.vehicle.trip.start_date
                            # Add other trip attributes as needed
                        },
                        'position': {
                            'latitude': entity.vehicle.position.latitude,
                            'longitude': entity.vehicle.position.longitude,
                            'bearing': entity.vehicle.position.bearing
                            # Add other trip attributes as needed
                        },
                        'position': {
                            'latitude': entity.vehicle.position.latitude,
                            'longitude': entity.vehicle.position.longitude,
                            'bearing': entity.vehicle.position.bearing,
                            'odometer': entity.vehicle.position.odometer,
                            'speed' : entity.vehicle.position.speed
                            # Add other trip attributes as needed
                        },
                        'stop_id': entity.vehicle.stop_id,
                        'current_status': entity.vehicle.current_status,
                        'timestamp': entity.vehicle.timestamp
                    }
                }


                # Append the entity dictionary to the list
                decoded_entities.append(entity_dict)

        # Convert the list of decoded entities to a JSON array
        json_array = json.dumps(entity_dict)
        # print(type(json_array))
        return json_array
    else:
        print(f"Error fetching coordinates: {response.status_code}")
        return None


def produce_kafka_messages():
    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER, 
                             api_version=(0,11,5),
                             value_serializer=lambda x: json.dumps(x).encode('utf-8'))

    while True:
        coordinates = fetch_coordinates()
        if coordinates:
            producer.send(TOPIC, value=coordinates)
            print(f"Message produced: {coordinates}")

        time.sleep(2)  # Wait for 5 seconds before fetching coordinates again

if __name__ == "__main__":
    produce_kafka_messages()