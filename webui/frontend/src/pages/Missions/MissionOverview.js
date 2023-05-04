import React, { Component } from 'react';
import { withRouter } from "react-router-dom";
import { connect } from "react-redux";
import { Button, Table } from "react-bootstrap";
import MissionModal from "./components/MissionModal";
import ApiHelper from "../../util/ApiHelper";


const pollInterval = 2000;

class MissionOverview extends Component {
  state = {
    missionModalOpen: false,
    missionModalData: null,
    lastMissionData: null,
    currentMissionData: null,
  };

  // Myself, if 
  checkDatabaseUpdates = async () => {
    const result = await ApiHelper.fetchTheNewestMission();
    if (!result) {
      alert("Error fetch the newest mission data.");
      return;
    }
    let lastData = this.state.lastMissionData;
    console.log("lastData", lastData)
    console.log("currentData", result)
    if (JSON.stringify(lastData) !== JSON.stringify(result)) {
      console.log('New data:', result);
      this.setState({ lastMissionData: result, currentMissionData: result });
      ApiHelper.fetchMissions().then();
    } else {
      console.log('No new data');
    }
  };

  componentDidMount() {
    ApiHelper.fetchMissions().then();
    this.checkDatabaseUpdates();
    
    this.intervalId = setInterval(() => {
      this.checkDatabaseUpdates();
    }, pollInterval);
  }

  componentWillUnmount() {
    clearInterval(this.intervalId);
  }

  openAddMission() {
    console.log("test")
    this.setState({
      missionModalOpen: true,
      missionModalData: null,
    });
  }

  /**
   * @param missionId  {string}
   */
  async openEditMission(missionId) {
    const missionData = await ApiHelper.fetchMissionById(missionId);
    console.log("open Modal")
    this.setState({
      missionModalOpen: true,
      missionModalData: missionData,
    });
  }

  async addMission(missionData) {
    console.log(" addMission check 1");
    this.setState({ missionModalOpen: false, missionModalData: missionData});

    // const result = await ApiHelper.fetchTheNewestMission();
    // this.setState({ lastMissionData: result, currentMissionData: result});

    console.log(" addMission check 2");

    await ApiHelper.createMission(missionData)
    // if (!await ApiHelper.createMission(missionData)) {
    //   alert("Error creating new mission");
    // }
    console.log(" addMission check 3");

    ApiHelper.fetchMissions().then();
  }

  /**
   * @param missionData
   */
  async updateMission(missionData) {
    this.setState({ missionModalOpen: false, missionModalData: missionData});
    // const result = await ApiHelper.fetchTheNewestMission();
    // this.setState({ lastMissionData: result, currentMissionData: result});

    const result = await ApiHelper.updateMission(missionData);

    // if (!result) {
    //   alert("Error updating mission: " + missionData["ueId"]);
    // }
    ApiHelper.fetchMissions().then();
  }

  /**
  * @param mission  {Tenant}
   */
  async deleteMission(mission) {
    if (!window.confirm(`Delete mission ${mission.missionName}?`))
      return;

    const result = await ApiHelper.deleteMission(mission.missionId);
    ApiHelper.fetchMissions().then();
    if (!result) {
      alert("Error deleting mission: " + mission.missionId);
    }
  }

  render() {
    return (
      <div className="container-fluid">
        <div className="row">
          <div className="col-md-12">
            <div className="card">
              <div className="header subscribers__header">
                <h4>Missions</h4>
                <Button bsStyle={"primary"} className="subscribers__button"
                  onClick={this.openAddMission.bind(this)}>
                  New Mission
                </Button>
              </div>
              <div className="content subscribers__content">
                <Table className="subscribers__table" striped bordered condensed hover>
                  <thead>
                    <tr>
                      <th style={{ width: 400, textAlign: 'center' }}>Mission ID</th>
                      <th colSpan={2} style={{ textAlign: 'center' }}>Mission Name</th>
                      {/* <th colSpan={3} style={{ textAlign: 'center' }}>Mission Coordinate</th> */}
                      <th colSpan={3} style={{ textAlign: 'center' }}>Longitude</th>
                      <th colSpan={4} style={{ textAlign: 'center' }}>Latitude</th>
                      <th colSpan={5} style={{ textAlign: 'center' }}>Settings</th>
                    </tr>
                  </thead>
                  <tbody>
                    {this.props.missions.map(mission => (
                      <tr key={mission.missionId}>
                        <td colSpan={1}>  {mission.missionId}</td>
                        <td colSpan={2}>  {mission.missionName}</td>
                        {/* <td colSpan={3}>  {mission.missionCoordinate}</td> */}
                        <td colSpan={3}>  {mission.MYSELF_Longitude}</td>
                        <td colSpan={4}>  {mission.MYSELF_Latitude}</td>
                        <td colSpan={5} style={{ textAlign: 'center' }}>
                          <Button variant="danger" onClick={this.deleteMission.bind(this, mission)}>Delete</Button>
                         &nbsp;&nbsp;&nbsp;&nbsp;
                        <Button variant="info" onClick={this.openEditMission.bind(this, mission.missionId)}>Modify</Button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </Table>

                <p>&nbsp;</p><p>&nbsp;</p>
                <p>&nbsp;</p><p>&nbsp;</p>
                <p>&nbsp;</p><p>&nbsp;</p>
              </div>
            </div>
          </div>
        </div>

        <MissionModal open={this.state.missionModalOpen}
          setOpen={val => this.setState({ missionModalOpen: val })}
          mission={this.state.missionModalData}
          onModify={this.updateMission.bind(this)}
          onSubmit={this.addMission.bind(this)} />
      </div>
    );
  }
}

const mapStateToProps = state => ({
  missions: state.mission.missions, // state.mission.missions is named in "redux > actions > missionActions" and "redux > reducers > mission"
                                   // state.mission is in "redux > reducers > mission"
});

export default withRouter(connect(mapStateToProps)(MissionOverview));
