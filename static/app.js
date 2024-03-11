let map = L.map('map', {
    layers: MQ.mapLayer(),
    center: [0, 0], // Set the center to [0, 0] to show the whole world
    zoom: 1 // Set the zoom level to 1 to show the whole world
});


var greenIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
    });

const dict = {
        long: 0,
        lat: 0
    }
const lat = document.getElementById("lat")
const long = document.getElementById("long")
const submitBtn = document.getElementById('submit')
submitBtn.addEventListener('click', e => {
        e.preventDefault()
        const marker1 = L.marker([dict.lat, dict.long], {icon: greenIcon}).bindPopup('You are here').addTo(map).openPopup();
        map.setView([dict.lat, dict.long], 13);
    })
lat.addEventListener('change', (e) => {
        dict.lat = +e.target.value

    })
long.addEventListener('change', e => {
        dict.long = +e.target.value
    })

// Define realtime marker

const ws = new WebSocket("ws://localhost:8000/ws");

ws.onmessage = function (event) {
    const measurement = JSON.parse(event.data);

    // Create a marker and a circle for the measurement
    const marker = L.marker([measurement.vehicle.position.latitude, measurement.vehicle.position.longitude]);
    const circle = L.circle([measurement.vehicle.position.latitude, measurement.vehicle.position.longitude], { radius: 4 });
    // Remove the oldest marker and circle from the map if there are more than 1 markers
    if (markers.length > 0) {
        map.removeLayer(markers[0]);
        map.removeLayer(circles[0]);
        markers.shift();
        circles.shift();
    }

    // Add the new marker and circle to the map
    markers.push(marker);
    circles.push(circle);
    marker.addTo(map);
    circle.addTo(map);

    // Fit the map bounds to the bounds of the markers
    L.featureGroup(markers);
};

// Initialize the arrays to store the markers and circles
const markers = [];
const circles = [];