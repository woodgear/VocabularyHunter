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

  constructor(props) {
    super(props)
    this.api = new Api(this.props.userId, this.props.vhServer)
    this.state = { article: '', explains: [], words: [], current_explain_index: 0 }
    this.actions = {
      markKnow: async word => {
        await this.api.markAsKnow([word])
        console.log('markKnow', word)
      },
      markUnKnow: async word => {
        await this.api.markAsUnKnow([word])
      },
      getMoreExplain: async (step) => {
        const words = this.state.words;
        const current_explain_index = this.state.current_explain_index;
        const end_index = current_explain_index + step < words.length ? current_explain_index + step : words.length;
        const explains = await this.api.getExplain(words.slice(current_explain_index, end_index));
        const filledExplains = this.state.explains.concat(explains);

        this.setState({ explains: filledExplains, current_explain_index: end_index })
      }
    }
  }

  componentDidMount() {
    console.log("load popup");
    bt.sendToContentScript({ action: 'parser' }).then(async (article) => {
      if (article) {
        const words = await this.api.hunter(article.content)
        this.setState({ words: words })
        this.actions.getMoreExplain(10);
      } else {
        console.log('??? why undefine ???')
      }
    })
  }

  render() {
    return (
      <div className="App">
        <DictContainer explains={this.state.explains} totalExplainsLength={this.state.words.length} actions={this.actions} />
      </div>
    )
  }
}

export default PopUp
