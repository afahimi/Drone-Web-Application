import React, { Component, useState, Fragment, useEffect } from "react";
// import Switch from "../Switch";
import { Grid, Switch, FormControlLabel} from "@material-ui/core";
import CssBaseline from "@material-ui/core/CssBaseline";
import { MuiThemeProvider, createMuiTheme } from "@material-ui/core/styles";


// import Feed from "./../../fetched-images/images/feed.png"
// import image3by2 from "../images/3-2.png"
// import Map1 from "./../../fetched-images/map1.png"

const MODES = Object.freeze({
  AUTOMATIC: 0,
  MANUAL: 1,
});

const MISSION = Object.freeze({
  USC_2022_TASK_1: 0,
  USC_2022_TASK_2: 1,
});

const styles = {
  fontSize: '30px',
  fontWeight: "bold",
};


const Toggle = () => {
  const [toggleStatus, setToggleStatus] = useState(0);
  const [MissionStatus, setMissionStatus] = useState(0);
  const [largestIndex, setLargestIndex] = useState(0);

  // //<img src= {this.imageIterator()}/>
  // const imageIterator = () => {
  //   for(var i = 1;;i++){
  //     if(i > 10){
  //       i = 1;
  //     }
  //     return '/images/'+ i +'.jpg';
  //   }
  // }

  useEffect(() => {
    // console.log("hi")
    setInterval(() => {
      fetch("http://localhost:6923/largest").then(response => {
        //TODO: make sure this doesnt crash
        // console.log(response);
        return response.text();
        }).then(largestIndex => {
          // console.log(largestIndex);
          setLargestIndex(largestIndex);
        }).catch(err => {
          console.log(err);
        });
    },100);
  },[]);


  const handleKeyPress = () => {
      if(MissionStatus === MISSION.USC_2022_TASK_2){
        setMissionStatus(MISSION.USC_2022_TASK_1);
      }
      else if(MissionStatus === MISSION.USC_2022_TASK_1){
        setMissionStatus(MISSION.USC_2022_TASK_2);
      }
      const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mission: MissionStatus })
      };
  
      fetch("http://localhost:6923/missionstatus", requestOptions)
  }

  const changeMode = () => {
    if(toggleStatus === MODES.AUTOMATIC){
      setToggleStatus(MODES.MANUAL);
    }
    else if(toggleStatus === MODES.MANUAL){
      setToggleStatus(MODES.AUTOMATIC);
    }
    
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mode: toggleStatus })
    };

    fetch("http://localhost:6923/controlmode", requestOptions)
}
  
  const buttonUpdate = () => {
        if(toggleStatus === MODES.AUTOMATIC){
            return "badge bg-success m-2";
        }

        else if(toggleStatus === MODES.MANUAL){
            return "badge bg-danger m-2";
        }

  }

  const statusCheck = () => {

      if(toggleStatus === MODES.AUTOMATIC){
          return "Automatic-Mode";
      }

      else if(toggleStatus === MODES.MANUAL){
          return "Manual-Mode";
      }
  }

  return ( 
    <Fragment>
      <Grid id = "top-row" container lg={12}s>
        <Grid item xs={6}>
          {/* <ImageThing/> */}
          <img src={`../fetched-images/${largestIndex}.jpg`} alt='not map'/>
        </Grid>
        {/* <Grid item xs={6}>
          <img src="http://localhost:3000/3-2.png" alt='map'/>
        </Grid> */}
      </Grid>
    
      <Grid id = "middle-row" container xs={12}>
        <Grid item xs={4}>
          <FormControlLabel control={<Switch defaultChecked />} label="Change Mode" onChange = {changeMode}/>
        </Grid>
        <Grid item xs={4}>
          <FormControlLabel control={<Switch defaultChecked />} label="USC MISSION 1 OR 2" onChange = {handleKeyPress}/>
        </Grid>
      </Grid>

      <Grid id = "bottom-row" container xs={12}>
        <Grid item xs={3}>
          <span style={styles} className={buttonUpdate()}>{statusCheck()}</span>
        </Grid>
        <Grid item xs={3}>
          <span style={styles} className="badge bg-primary">Controller Connected</span>
        </Grid>
      </Grid>
    </Fragment>

    /* // <Grid id = "top row" container xs={12}>
    //   <Grid item xs={4}>
    //     <span style={styles} className={buttonUpdate()}>{statusCheck()}</span>
    //   </Grid>
    //   <Grid item xs={4}>
    //     <FormControlLabel control={<Switch defaultChecked />} label="TEST" onChange = {handleKeyPress}/>
    //   </Grid>

    // </Grid>
    
    // <Grid container spacing={0} direction="column" allignItems="center" justifyContent="center" style={{ minHeight: '100vh' }}>
      
    // </Grid>
    // <div style={{padding, left, top,position:'absolute'}}>
    //   <span style={this.styles} className={this.buttonUpdate()}>{this.statusCheck()}</span>
    //   <button onClick={this.handleKeyPress} style={this.styles} className="button btn-secondary btn-lg">CHANGE MODE</button>
    //   
    // </div> */
  );
}

export default Toggle;