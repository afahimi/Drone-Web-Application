import React, { Component } from "react";
import Switch from "../Switch";
import { Grid } from "@mui/material";

const styles = {
  fontSize: '30px',
  fontWeight: "bold",
};

const Toggle = () => {
  var left = 100 + 'px';
  var top = 100 + 'px';
  var padding = 100 + 'px';
    
  const imageIterator = () => {
    for(var i = 1;;i++){
      if(i > 10){
        i = 1;
      }
      return '/images/'+ i +'.jpg';
    }
  }

  const handleKeyPress = () => {
    console.log("Clicked!");
    if(this.state.status === 0){
      this.setState({status: 1});
    }
    else if(this.state.status === 1){
      this.setState({status: 0});
    }
  }

  const buttonUpdate = () => {
    console.log("Clicked!");
    
    if(this.state.status === 0){
        return "badge bg-success m-2";
    }

    else if(this.state.status === 1){
        return "badge bg-danger m-2";
    }
  }

  const statusCheck = () => {
      if(this.state.status === 0){
          return "Automatic-Mode";
      }

      else if(this.state.status === 1){
          return "Manual-Mode";
      }
  }

  return ( 
    // <div style={{padding, left, top,position:'absolute'}}
    <Grid container xs={12}>
      <Grid item xs={4}>
        <span style={this.styles} className={this.buttonUpdate()}>{this.statusCheck()}</span>
      </Grid>
      <Grid item xs={4}>
        <button onClick={this.handleKeyPress} style={this.styles} className="button btn-secondary btn-lg">CHANGE MODE</button>
      </Grid>
      <Grid item xs={4}>
        <Switch/>
      </Grid>
    </Grid>
  );
}

export default Toggle;
