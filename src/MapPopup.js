import React, {Component} from 'react';
import { Popup } from 'react-mapbox-gl';

export default class MapPopup extends Component {
  constructor(props) {
    super(props);

    this.state = {
      show: false,
      coordinates: [-79.232, 43.725],
      specs: [],
      excs: []
    }
  }

  show = () => {
    this.setState({
      show: true
    });
  }

  setCoordinates = (new_coords) => {
    this.setState({
      coordinates: new_coords
    })
  }

  setSpecs = (new_specs) => {
    this.setState({
      specs: new_specs
    })
  }

  setExcs = (new_excs) => {
    this.setState({
      excs: new_excs
    })
  }

  getPath = () => {
    console.log(this.state.specs);
    let areaQuery = 'area=cliffcrest';
    let specQuery = `specifications=${this.state.specs}`;
    let excQuery = `exceptions=${this.state.excs}`;
    let fullQuery = [areaQuery, specQuery, excQuery].join('&')
    return `/bylaws?${fullQuery}`;
  }

  render() {
    let text = String(this.state.specs) + String(this.state.excs);
    return (
      <>
        {this.state.show && <Popup coordinates={this.state.coordinates}>
          <a href={this.getPath()}>{text}</a>
        </Popup>}
      </>
    )
  }
}
