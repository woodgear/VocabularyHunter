import React from 'react'
import ReactDOM from 'react-dom'
import OptionPage from './optionPage'
import init from '../../../init'

init().then(({ userId, vhServer }) => {
  ReactDOM.render(<OptionPage userId ={userId} vhServer={vhServer}/>, document.getElementById('root'))
})
