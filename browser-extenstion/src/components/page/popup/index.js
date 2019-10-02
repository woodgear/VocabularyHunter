import React from 'react';
import ReactDOM from 'react-dom';
import PopUp from './popup';
import init from "../../../init";
init().then(({ userId, vhServer }) => {
    ReactDOM.render(<PopUp userId={userId} vhServer={vhServer} />, document.getElementById('root'));

})