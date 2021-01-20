import React, {Component} from 'react';
import ReactMapboxGl, { GeoJSONLayer } from 'react-mapbox-gl';
import axios from 'axios';
import MapPopup from './MapPopup.js';

const Map = ReactMapboxGl({
  accessToken:
    'pk.eyJ1IjoiYnVzaW5lc3Nqb2UiLCJhIjoiY2tiMmFoeHc2MGMxcDJxcjFrNDVveHczYiJ9.quq-o1ig6VHAEPPzLbjkJQ'
});

export default class MapComponent extends Component {
  constructor(props) {
    super(props);

    this.popup = React.createRef();
    this.state = {};
  }

  get_geojson(area) {
    axios.get(`/dxf/geojson/${area}/`)
    .then(response => {
      let features = response.data.map(f => {
        f.properties.codes = f.properties.codes.join();
        return f
      });

      this.setState({
        spec_geojson: {
          type: 'FeatureCollection',
          features: features.filter(f => f.properties.bylaw_type === 'spec')
        },
        exc_geojson: {
          type: 'FeatureCollection',
          features: features.filter(f => f.properties.bylaw_type === 'exc')
        }
      });
    });
  }

  componentDidMount() {
    this.get_geojson('cliffcrest');
  }

  render() {
    let specPolygonPaint = ReactMapboxGl.FillPaint = {
      'fill-color': "#0000ff",
      'fill-opacity': 0.3
    }
    let excPolygonPaint = ReactMapboxGl.FillPaint = {
      'fill-color': "#ff0000",
      'fill-opacity': 0.3
    }


    return (
      <Map
        style="mapbox://styles/mapbox/streets-v11"
        containerStyle={{
          height: '100vh',
          width: '100vw'
        }}
        center={[-79.232, 43.725]}
        zoom={[13]}
      >
        <GeoJSONLayer
          data={this.state.spec_geojson}
          fillPaint={specPolygonPaint}
          fillOnClick={(e) => {
            this.popup.current.show();
            this.popup.current.setCoordinates([e.lngLat.lng, e.lngLat.lat]);
            this.popup.current.setSpecs(e.features.flatMap(f => f.properties.codes));
          }}
        />
        <GeoJSONLayer
          data={this.state.exc_geojson}
          fillPaint={excPolygonPaint}
          fillOnClick={(e) => {
            this.popup.current.show();
            this.popup.current.setCoordinates([e.lngLat.lng, e.lngLat.lat]);
            this.popup.current.setExcs(e.features.flatMap(f => f.properties.codes));
          }}
        />
        <MapPopup ref={this.popup}/>
      </Map>
    );
  }
}
