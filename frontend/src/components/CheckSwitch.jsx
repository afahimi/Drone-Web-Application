import React, { Component } from 'react';
import Switch from "../Switch";

class CheckSwitch extends Component {
    state = {}
    render() {
        var left = 50 + 'px';
        var top = 50 + 'px';
        var padding = 50 + 'px';
        return (
            <div style={{ padding, left, top, position: 'absolute' }}><Switch /></div>
        );
    }
}

export default CheckSwitch;