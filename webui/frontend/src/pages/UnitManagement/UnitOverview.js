import React, { Component } from "react";
import { withRouter } from "react-router-dom";
import { connect } from "react-redux";
import { Button } from "react-bootstrap";
import UnitModal from "./components/UnitModal";
import DeviceModal from "./components/DeviceModal";
import ApiHelper from "../../util/ApiHelper";
import { BootstrapTable, TableHeaderColumn } from "react-bootstrap-table";
import OnlineApiHelper from "../../util/OnlineApiHelper";

class UnitOverview extends Component {
  state = {
    unitModalOpen: false,
    subscriberModalData: null,
    deviceModalOpen: false,
    deviceModalData: null,
    deviceModalUnit: null,
    unselectable: [],
    selected: [],
  };

  componentDidMount() {
    // ApiHelper.fetchRegisteredUnits().then();
    OnlineApiHelper.fetchOnlineUnit().then();
  }

  openAddUnit() {
    this.setState({
      unitModalOpen: true,
      subscriberModalData: null,
    });
  }

  /**
   * @param subscriberId  {number}
   * @param plmn          {number}
   */
  async openAddDevice(id) {
    OnlineApiHelper.fetchOnlineDevice().then();
    OnlineApiHelper.fetchOnlineUnit().then();
    // ApiHelper.fetchRegisteredDevices().then();
    // ApiHelper.fetchRegisteredUnits().then();

    // console.log("this.props.devices", this.props.devices);

    let unselectable = [];
    let selected = [];

    this.props.units.forEach((unit) => {
      unit.Members.forEach((element) => {
        if (unit.UnitName == id) {
          selected.push(element.DeviceName);
        } else {
          unselectable.push(element.DeviceName);
        }
        // console.log("members element", element.DeviceName);
        // if (element.UnitId != id) {
        //   unselectable.push(element.DeviceName)
        // }
        // else {
        //   selected.push(element.DeviceName)
        // }
      });
    });

    this.setState({
      deviceModalOpen: true,
      // deviceModalData: deviceData,
      deviceModalUnit: id,
      unselectable: unselectable,
      selected: selected,
    });
  }

  async addDevice(selectMap) {
    // this.setState({ deviceModalOpen: false });
    // let userNumber = subscriberData["userNumber"];
    // delete subscriberData["userNumber"];
    // let imsiLength = subscriberData["ueId"].length - 5;
    // let imsi = subscriberData["ueId"].substr(5, imsiLength);
    // for (let i = 0; i < userNumber; i++) {
    //   let newImsi = (Number(imsi) + i).toString();
    //   newImsi = newImsi.padStart(imsiLength, "0");
    //   subscriberData["ueId"] = `imsi-${newImsi}`;
    //   if (!(await ApiHelper.createSubscriber(subscriberData))) {
    //     alert("Error creating new subscriber when create user");
    //   }
    //   ApiHelper.fetchSubscribers().then();
    // }
    this.setState({ deviceModalOpen: false });

    console.log("selectMap", selectMap)
  }

  async updateDevice(selectMap, unitName) {
    this.setState({ deviceModalOpen: false });

    console.log("selectMap", selectMap)

    for (let [key, value] of selectMap) {
      if (value) {
        ApiHelper.addDeviceToUnit(key, unitName)
      }
      else {
        ApiHelper.deleteDeviceFromUnit(key, unitName)
      }
    }
    // const result = await ApiHelper.updateSubscriber(subscriberData);

    // if (!result) {
    //   alert("Error updating subscriber: " + subscriberData["ueId"]);
    // }
    // ApiHelper.fetchSubscribers().then();
    OnlineApiHelper.fetchOnlineUnit().then();
    
  }

  async addUnit(unitData) {
    this.setState({ unitModalOpen: false });

    if (!(await ApiHelper.createRegisteredUnit(unitData))) {
      alert("Error creating new unit");
    }
    OnlineApiHelper.fetchOnlineUnit().then();
  }

  /**
   * @param subscriberData
   */
  async updateSubscriber(subscriberData) {
    this.setState({ subscriberModalOpen: false });

    const result = await ApiHelper.updateSubscriber(subscriberData);

    if (!result) {
      alert("Error updating subscriber: " + subscriberData["ueId"]);
    }
    ApiHelper.fetchSubscribers().then();
  }

  async deleteUnit(UnitName) {
    if (!window.confirm(`Delete unit ${UnitName}?`)) return;

    const result = await ApiHelper.deleteRegisteredUnit(UnitName);
    if (!result) {
      alert("Error deleting unit: " + UnitName);
    }
    OnlineApiHelper.fetchOnlineUnit().then();
  }

  render() {
    return (
      <div className="container-fluid">
        <div className="row">
          <div className="col-md-12">
            <div className="card">
              <div className="header subscribers__header">
                <h1>Unit Management</h1>
              </div>
              <div className="header subscribers__header">
                <h3>Registered Units</h3>
                <Button
                  bsStyle={"primary"}
                  className="subscribers__button"
                  onClick={this.openAddUnit.bind(this)}
                >
                  New Unit
                </Button>
              </div>
              <div
                className="content subscribers__content"
                style={{ "overflow-y": "scroll", height: "600px" }}
              >
                {!this.props.get_unit_err && (
                  <BootstrapTable
                    data={this.props.units}
                    striped={true}
                    hover={true}
                  >
                    <TableHeaderColumn
                      row="0"
                      rowSpan="2"
                      dataField="UnitId"
                      width="20%"
                      isKey={true}
                      dataAlign="center"
                      dataSort={true}
                    >
                      Unit ID
                    </TableHeaderColumn>
                    <TableHeaderColumn
                      row="0"
                      rowSpan="2"
                      dataField="UnitName"
                      width="20%"
                      dataAlign="center"
                      dataSort={true}
                    >
                      Unit Name
                    </TableHeaderColumn>
                    <TableHeaderColumn
                      row="0"
                      rowSpan="2"
                      dataField="BitrateLimit"
                      width="20%"
                      dataAlign="center"
                      dataSort={true}
                    >
                      Bitrate Limit
                    </TableHeaderColumn>
                    <TableHeaderColumn row="0" colSpan="2" headerAlign="center">
                      Operation
                    </TableHeaderColumn>
                    <TableHeaderColumn
                      row="1"
                      dataField="UnitName"
                      width="10%"
                      dataAlign="center"
                      dataFormat={(cell, row, rowIndex, formatExtraData) => {
                        return (
                          <Button
                            bsClass="btn-info"
                            onClick={this.openAddDevice.bind(this, cell)}
                          >
                            Add
                          </Button>
                        );
                      }}
                    >
                      Add Device
                    </TableHeaderColumn>
                    <TableHeaderColumn
                      row="1"
                      dataField="UnitName"
                      width="10%"
                      dataAlign="center"
                      dataFormat={(cell, row, rowIndex, formatExtraData) => {
                        return (
                          <Button
                            bsClass="btn-danger"
                            onClick={this.deleteUnit.bind(this, cell)}
                          >
                            Delete
                          </Button>
                        );
                      }}
                    >
                      Delete Unit
                    </TableHeaderColumn>
                  </BootstrapTable>
                )}
                {this.props.get_unit_err && <h2>{this.props.unit_err_msg}</h2>}
              </div>
            </div>
          </div>
        </div>

        <UnitModal
          open={this.state.unitModalOpen}
          setOpen={(val) => this.setState({ unitModalOpen: val })}
          subscriber={this.state.subscriberModalData}
          onSubmit={this.addUnit.bind(this)}
        />

        <DeviceModal
          open={this.state.deviceModalOpen}
          setOpen={(val) => this.setState({ deviceModalOpen: val })}
          alldevice={this.state.deviceModalData}
          onModify={this.updateDevice.bind(this)}
          onSubmit={this.addDevice.bind(this)}
          unit={this.state.deviceModalUnit}
          unselectable={this.state.unselectable}
          selected={this.state.selected}
        />
      </div>
    );
  }
}

const mapStateToProps = (state) => ({
  units: state.online.units,
  get_unit_err: state.online.get_unit_err,
  unit_err_msg: state.online.unit_err_msg,

  devices: state.online.devices,
});

export default withRouter(connect(mapStateToProps)(UnitOverview));
