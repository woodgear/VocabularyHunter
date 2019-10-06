import './optionPage.css'
import React, { Component } from 'react'
import PropTypes from 'prop-types'
import Api from '../../../api'
import * as bt from '../../../browser/browser_tool'

import { saveAs } from 'file-saver'

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

  renderExportAndImport () {
    return (<div>
      <button onClick={async () => {
        const api = new Api(this.state.userId, this.state.vhServer)
        const data = await api.export()
        var blob = new Blob([JSON.stringify(data)], { type: 'application/json;charset=utf-8' })
        saveAs(blob, 'export.json')
      }}>导出</button>

      <input type="file" id="input" onChange={async (event) => {
        const jsonFile = event.target.files[0]
        console.log(jsonFile)
        const context = JSON.parse(await jsonFile.text())
        const words = context.words
        const api = new Api(this.state.userId, this.state.vhServer)
        console.log('start upload')
        await api.import(words)
        console.log('upload over')
      }} />

    </div>)
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
          {this.renderExportAndImport()}
        </div>

      </div>)
  }
}

export default OptionPage
