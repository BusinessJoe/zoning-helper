$(document).ready(function() {
    // send request to map/zones which returns all of the zone's geojson
    $.get('zones', function(data, status) {
        console.log(status);
        console.log(data);

        load_map(data['specifications'], data['exceptions']);
    });
});

function load_map(specificationZones, exceptionZones) {
    var mymap = L.map('map').setView([43.725, -79.232], 17);
    var mapboxUrl = 'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}';
    var attribution = 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>';

    var street_id = 'mapbox/streets-v11'
    var sat_id = 'mapbox/satellite-v9'

    L.tileLayer(mapboxUrl, {
        attribution: attribution,
        maxZoom: 18,
        id: street_id,
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'pk.eyJ1IjoiYnVzaW5lc3Nqb2UiLCJhIjoiY2tiMmFoeHc2MGMxcDJxcjFrNDVveHczYiJ9.quq-o1ig6VHAEPPzLbjkJQ'
    }).addTo(mymap);

    var popup = L.popup();

    function zoneFromPoint(point, layer) {
        return leafletPip.pointInLayer(point, layer, true)
    }

    function getZonePopupHtml(e, layerType) {
        if (layerType == 'spec') {
            path = 'specifications';
            layer = specLayer;
        }
        else if (layerType == 'exc') {
            path = 'exceptions';
            layer = excLayer;
        }

        var match = zoneFromPoint(e.latlng, layer);
        if (match.length != 0) {
            var standard = match[0].feature.geometry.zone_spec;
            var html = `<a href="/bylaw/${path}/${standard}" target="_blank">${standard}</a>`;
            return html;
        }
        return ''
    }

    function onMapClick(e) {
        var specHtml = getZonePopupHtml(e, "spec");
        var excHtml = getZonePopupHtml(e, "exc");

        if (specHtml !== '' || excHtml !== '') {        
            var html = `<h3>Spec: ${specHtml}<br>Exc: ${excHtml}</h3>`;

            popup
                .setLatLng(e.latlng)
                .setContent(html)
                .openOn(mymap);
        }
        else {
            mymap.closePopup();
        }
    }

    mymap.on('click', onMapClick);


    var specLayer = L.geoJSON(specificationZones, {
    
    });

    var excLayer = L.geoJSON(exceptionZones, {
        style: {
            'color': '#FF4500'
        }
    });

    var overlays = {
        '<span class="layername">Specifications</span>': specLayer,
        '<span class="layername">Exceptions</span>': excLayer
    };

    // Add layers so that they're visible by default
    excLayer.addTo(mymap);
    specLayer.addTo(mymap);
    //L.control.layers(null, overlays, {collapsed: false, position: 'topleft'}).addTo(mymap);
}
