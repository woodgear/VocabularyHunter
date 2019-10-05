import './optionPage.css'
import React, { Component } from 'react'
import PropTypes from 'prop-types'

import * as bt from '../../../browser/browser_tool'

async function setUserId (userId) {
  console.log('setUserId', userId)
  return bt.setStorage('userId', userId)
}

async function setVhServer (vhServer) {
  console.log('setVhServer', vhServer)
  return bt.setStorage('vhServer', vhServer)
}

class OptionPage extends Component {
  static propTypes = {
    userId: PropTypes.string,
    vhServer: PropTypes.string
  };

  constructor (props) {
    super(props)
    this.state = { userId: this.props.userId, vhServer: this.props.vhServer, debugMode: false }
  }

  render () {
    return (
      <div className="app">
        <div className="input-container user-id">
          <span className="name">user id:</span>
          <input className="input" type="text" disabled={!this.state.debugMode} onInput={(event) => {
            this.setState({ userId: event.target.value })
          }} defaultValue={this.state.userId} />
          <button className="action" hidden={!this.state.debugMode} onClick={() => {
            setUserId(this.state.userId)
          }}>确定</button>

        </div>
        <div className="input-container vh-server">
          <span className="name">vh server:</span>
          <input className="input" type="text" disabled={!this.state.debugMode} onInput={(event) => {
            this.setState({ vhServer: event.target.value })
          }} defaultValue={this.state.vhServer} />
          <button className="action" hidden={!this.state.debugMode} onClick={() => {
            setVhServer(this.state.vhServer)
          }}>确定</button>
        </div>
        <div>
          <input type="checkbox" id="debug-mode-checkbox" defaultChecked={!this.state.debugMode} name="debug-mode" onClick={() => {
            console.log('oncheck')
            this.setState({ debugMode: !this.state.debugMode })
          }} />
          <label >debug-mode</label>
        </div>

      </div>)
  }
}

export default OptionPage
