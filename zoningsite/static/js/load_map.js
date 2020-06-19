$(document).ready(function() {

    // send request to map/zones which returns all of the zone's geojson
    $.get('zones', function(data, status) {
        console.log(status);
        console.log(data);
        var zones = data;

        load_map(zones);
    });
});

function load_map(zones) {
    var mymap = L.map('mapid').setView([43.725, -79.232], 17);

    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'pk.eyJ1IjoiYnVzaW5lc3Nqb2UiLCJhIjoiY2tiMmFoeHc2MGMxcDJxcjFrNDVveHczYiJ9.quq-o1ig6VHAEPPzLbjkJQ'
    }).addTo(mymap);


    function onClick(e) {
        console.log(e);
    }

    function onEachFeature(feature, layer) {
        layer.bindPopup('<h1><a href="/bylaw/' + feature.zone_spec + '" target="_blank">' + feature.zone_spec + '</a></h1>');
        console.log(feature);
    }

    L.geoJSON(zones, {
        onEachFeature: onEachFeature
    }).addTo(mymap);
};