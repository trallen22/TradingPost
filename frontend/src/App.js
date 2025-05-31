import './App.css';
// import ReactDOM from "react-dom/client";
import {
    BrowserRouter as Router,
    Routes,
    Route,
	Navigate,
} from "react-router-dom";
import Home from './pages/home';

function App() {
  return (
    <div className="App">
			<Router>
				<Routes>
					<Route
						path="/*"
						element={<Home />}
					></Route>
				</Routes>
			</Router>
		</div>
  );
}

export default App;
