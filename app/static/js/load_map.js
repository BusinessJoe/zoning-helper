$(document).ready(function() {
    // send request to map/zones which returns all of the zone's geojson
    $.get('zones', function(data, status) {
        console.log(status);
        console.log(data);

        load_map(data['specifications'], data['exceptions']);
    });
});

// Adds a .curry method to functions
function toArray(en) {
    return Array.prototype.slice.call(en);
}

Function.prototype.curry = function() {
    if (arguments.length<1) {
        return this; //nothing to curry with - return function
    }
    var __method = this;
    var args = toArray(arguments);
    return function() {
        return __method.apply(this, args.concat(toArray(arguments)));
    }
}

function zoneFromPoint(point, layer) {
    return leafletPip.pointInLayer(point, layer, true)
}

function getZonePopupHtml(e, layerType, layer) {
    var match = zoneFromPoint(e.latlng, layer);


    if (match.length != 0) {
        var zone = match[0];
        var area = zone.feature.geometry.area;
        var standard = zone.feature.geometry.zone_spec;
        var zone_id = zone.feature.geometry.zone_id;

        var html = `<a href="/bylaw/${layerType}/${area}/${zone_id}" target="_blank">${standard}</a>`;
        return html;
    }
    return ''
}

function onMapClick(map, specLayer, excLayer, e) {
    var specHtml = getZonePopupHtml(e, "specifications", specLayer);
    var excHtml = getZonePopupHtml(e, "exceptions", excLayer);

    if (specHtml !== '' || excHtml !== '') {        
        var html = `<h3>Spec: ${specHtml}<br>Exc: ${excHtml}</h3>`;

        var popup = L.popup();
        popup
            .setLatLng(e.latlng)
            .setContent(html)
            .openOn(map);
    }
    else {
        map.closePopup();
    }
}

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


    var specLayer = L.geoJSON(specificationZones, {
    });

    var excLayer = L.geoJSON(exceptionZones, {
        style: {
            'color': '#FF4500'
        }
    });

    mymap.on('click', onMapClick.curry(mymap, specLayer, excLayer));

    var overlays = {
        '<span class="layername">Specifications</span>': specLayer,
        '<span class="layername">Exceptions</span>': excLayer
    };

    // Add layers so that they're visible by default
    excLayer.addTo(mymap);
    specLayer.addTo(mymap);
    L.control.layers(null, overlays, {collapsed: false, position: 'topleft'}).addTo(mymap);
}
