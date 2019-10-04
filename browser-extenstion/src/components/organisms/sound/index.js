import React, { Component } from "react";

import "./index.css";
import soudIcon from "./sound_wave.ico";
import { default as ReactSound,PlayStatus } from 'react-sound';

export default class Sound extends Component {
    constructor(props) {
        super(props);
        this.state = { playStatus: "STOPPED" };
    }
    render() {
        const soundUrl=`https://ssl.gstatic.com/dictionary/static/sounds/oxford/${this.props.word}--_gb_1.mp3`

return (<div className="sound">
            <img src={soudIcon} onClick={() => {
                console.log("on sound click");
                if (this.state.playStatus === "STOPPED") {
                    console.log("setState to PLAYING")
                    this.setState({ playStatus: "PLAYING"})
                }
                if (this.state.playStatus ==="PLAYING") {
                    this.setState({ playStatus: "PLAYING" })
                }
                if (this.state.playStatus === "PAUSED") {
                    this.setState({ playStatus: "PLAYING"})
                }
            }} />

            <ReactSound url={soundUrl}
                playStatus={this.state.playStatus}
                onFinishedPlaying={()=>{
                    this.setState({playStatus:"STOPPED"})
                }}
            />
        </div>)
    }
}