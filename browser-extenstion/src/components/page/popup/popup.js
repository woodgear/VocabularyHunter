import './popup.css'
import React, { Component } from 'react'
import DictContainer from '../../organisms/dictcontainer'
import Api from '../../../api'
import * as bt from '../../../browser/browser_tool'
import PropTypes from 'prop-types'

class PopUp extends Component {
  static propTypes = {
    userId: PropTypes.string,
    vhServer: PropTypes.string
  };

  constructor (props) {
    super(props)
    this.api = new Api(this.props.userId, this.props.vhServer)
    this.state = { article: '', explains: [] }
    this.actions = {
      markKnow: async word => {
        await this.api.markAsKnow([word])
        console.log('markKnow', word)
      },
      markUnKnow: async word => {
        await this.api.markAsUnKnow([word])
      }
    }
  }

  componentDidMount () {
    bt.sendToContentScript({ action: 'parser' }).then(async ({ article }) => {
      if (article) {
        console.log(article)
        const words = await this.api.hunter(article.content)
        const explains = await this.api.getExplain(words)
        console.log(explains)
        this.setState({ explains })
      } else {
        console.log('??? why undefine ???')
      }
    })
  }

  render () {
    return (
      <div className="App">
        <DictContainer explains={this.state.explains} actions={this.actions} />
      </div>
    )
  }
}

export default PopUp
