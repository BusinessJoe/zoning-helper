import React, {Component} from 'react';
import axios from 'axios';
axios.defaults.baseURL = 'http://localhost:8000';

export default class MapComponent extends Component {
  get_geojson(area) {
    var data = axios.get(`dxf/geojson/${area}/`);
    console.log(data);
  }

  render() {
    this.get_geojson('cliffcrest');
    return (
      <div>Hello world! This will be a map</div>
    );
  }
}
