import "./optionPage.css";
import React, { Component } from "react";

class OptionPage extends Component {

  constructor(props) {
    super(props);
    this.state = { userId: null, vh_server: null };
  }
  render() {
    return (
      <div className="App">
        <div className="user-id-container">
          <span>user id:</span>
          <input type="text" defaultValue={this.state.vh_server || "xxxx"} />
          {this.state.userId}
        </div>
        <div>
          <span>vh server:</span>
          <input type="text" defaultValue={this.state.vh_server || "xxxx"} />
          <button>确定</button>
        </div>
      </div>)
  }
}

export default OptionPage;
