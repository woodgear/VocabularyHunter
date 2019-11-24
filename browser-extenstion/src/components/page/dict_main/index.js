import React from 'react'
import ReactDOM from 'react-dom'
import DictMain from './dict_main'
import init from '../../../init'
init().then(({ userId, vhServer }) => {
  ReactDOM.render(<DictMain userId={userId} vhServer={vhServer} />, document.getElementById('root'))
})
