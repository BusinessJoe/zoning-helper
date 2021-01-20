import { HashRouter as Router, Route, Switch } from "react-router-dom";
import './App.css';
import MapComponent from './MapComponent.js';
import BylawViewer from './BylawViewerComponent.js';
import mapboxgl from 'mapbox-gl';

// eslint-disable-next-line import/no-webpack-loader-syntax
mapboxgl.workerClass = require('worker-loader!mapbox-gl/dist/mapbox-gl-csp-worker').default;

function App() {
  return (
    <Router basename="/static">
      <Switch>
        <Route path="/" exact component={MapComponent} />
        <Route path="/bylaws" component={BylawViewer} />
      </Switch>
    </Router>
  );
}

export default App;
