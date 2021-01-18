import React, {Component} from 'react';
import ReactMapboxGl, { Layer, Feature, GeoJSONLayer, Popup } from 'react-mapbox-gl';
import axios from 'axios';
axios.defaults.baseURL = 'http://localhost:8000';

const Map = ReactMapboxGl({
  accessToken:
    'pk.eyJ1IjoiYnVzaW5lc3Nqb2UiLCJhIjoiY2tiMmFoeHc2MGMxcDJxcjFrNDVveHczYiJ9.quq-o1ig6VHAEPPzLbjkJQ'
});

export default class MapComponent extends Component {
  constructor(props) {
    super(props);

    this.state = {
      popup: {
        show: false,
        coordinates: [-79.232, 43.725],
        text: null
      },
      geojson: null
    };
  }

  get_geojson(area) {
    console.log('getting');
    axios.get(`dxf/geojson/${area}/`)
    .then(response => {
      let features = [];
      response.data.forEach((feat) => {
        features.push(feat);
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
            let new_popup = {...this.state.popup};
            new_popup.show = true;
            new_popup.coordinates = [e.lngLat.lng, e.lngLat.lat];
            new_popup.text = e.features[0].properties.codes;
            console.log(e.features[0].properties.area);

            this.setState({
              popup: new_popup
            });
          }}
        />
        <GeoJSONLayer
          data={this.state.exc_geojson}
          fillPaint={excPolygonPaint}
          fillOnClick={(e) => {
            let new_popup = {...this.state.popup};
            new_popup.show = true;
            new_popup.coordinates = [e.lngLat.lng, e.lngLat.lat];
            new_popup.text = e.features[0].properties.codes;
            console.log(e.features[0].properties.area);

            this.setState({
              popup: new_popup
            });
          }}
        />
        {this.state.popup.show && <Popup
          coordinates={this.state.popup.coordinates}
        >
          <div>{this.state.popup.text}</div>
        </Popup>}
      </Map>
    );
  }
}
