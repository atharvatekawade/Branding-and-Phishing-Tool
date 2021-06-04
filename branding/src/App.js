import React from "react";
import { Route } from "react-router-dom";
//import Header from "./Components/Header";
import Similarity from "./Components/Similarity";
import Monitoring from "./Components/Monitoring";
import Phising from "./Components/Phising";
import Report from "./Components/Report";
import Home from "./Components/Home";

const App = () => {
  return (
    <div>
      <main className="py-3">
          <Route exact path="/" exact>
            <Home />
          </Route>
  
          <Route exact path="/monitoring" exact>
            <Monitoring/>
          </Route>

          <Route exact path="/phishing" exact>
            <Phising/>
          </Route>

          <Route exact path="/similarity" exact>
            <Similarity/>
          </Route>

          <Route exact path="/reporting" exact>
            <Report/>
          </Route>
         
        </main>

    </div>
  );
};

export default App;
