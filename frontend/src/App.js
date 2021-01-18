import { BrowserRouter as Router, Route } from "react-router-dom";
import './App.css';
import MapComponent from './MapComponent.js';
import BylawViewer from './BylawViewerComponent.js';

function App() {
  return (
    <Router>
      <Route path="/" exact component={MapComponent} />
      <Route path="/bylaws" component={BylawViewer} />
    </Router>
  );
}

export default App;
