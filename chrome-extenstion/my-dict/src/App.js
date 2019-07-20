import React from "react";
import "./App.css";
import DictContainer from "./components/dictcontainer";
import VhInput from "./components/VHInput";

function App() {
  return (
    <div className="App">
      <VhInput />
      <DictContainer />
    </div>
  );
}

export default App;
