import React, {Component} from 'react';
import qs from 'qs';
import axios from 'axios';
import BylawSpecification from './BylawSpecification.js';
import BylawException from './BylawException.js';
import './Bylaw.css';

export default class BylawViewer extends Component {
  constructor(props) {
    super(props);

    let params = qs.parse(this.props.location.search, {
      ignoreQueryPrefix: true, comma: true
    });
    // Convert params to arrays if they aren't an array.
    // A query string like a=1,2,3 produces the array ["1","2","3"] but
    // the string a=4 produces the string "4".
    let spec_codes = params.specifications ? params.specifications : [];
    spec_codes =  Array.isArray(spec_codes) ? spec_codes : [spec_codes];
    let exc_codes = params.exceptions ? params.exceptions : [];
    exc_codes =  Array.isArray(exc_codes) ? exc_codes : [exc_codes];

    this.state = {
      spec_codes: spec_codes,
      exc_codes: exc_codes,
      area: params.area ? params.area : null,
    };
  }


  render() {
    let specifications = this.state.spec_codes.map(
      (code, index) => (
        <BylawSpecification
          area={this.state.area}
          code={code}
          key={index}
        />
    ));

    let exceptions = this.state.exc_codes.map(
      (code, index) => (
        <BylawException
          area={this.state.area}
          code={code}
          key={index}
        />
    ));

    return (
      <div className="page-container">
        <div className="area-name">
          {this.state.area.charAt(0).toUpperCase() + this.state.area.slice(1)}
        </div>
        <div className="bylaw-container">
          {
            specifications.length !== 0 &&
            <div className="bylaw-type">Specifications</div>
          }
          {specifications}
        </div>
        <div className="bylaw-container">
          {
            exceptions.length !== 0 &&
            <div className="bylaw-type">Exceptions</div>
          }
          {exceptions}
        </div>
      </div>
    )
  }
}
