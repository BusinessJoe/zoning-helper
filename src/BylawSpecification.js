import React, {Component} from 'react';
import ReactHtmlParser from 'react-html-parser';
import axios from 'axios';
import './Bylaw.css';

axios.defaults.baseURL = 'http://localhost:8000';

export default class BylawException extends Component {
  constructor(props) {
    super(props);

    this.state = {
      data: {}
    };
  }

  componentDidMount() {
    this.get_specification();
  }

  get_specification() {
    axios.get(`dxf/bylaw/spec/${this.props.area}/${this.props.code}/`)
    .then(({data}) => {
      this.setState({
        data: data
      });
    })
    .catch(err => {
      this.setState({
        data: {
          context: "ERROR",
          code: this.props.code,
          text: "Requested code was not found."
        }
      });
    });
  }

  render() {
    return (
      <div className="bylaw">
        <div><b>{this.state.data.context}:</b> {this.state.data.code}</div>
        <div>{ReactHtmlParser(this.state.data.text)}</div>
      </div>
    );
  }
}
