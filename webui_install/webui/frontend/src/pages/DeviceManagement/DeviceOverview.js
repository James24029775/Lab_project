import React, { Component } from "react";
import { withRouter } from "react-router-dom";
import { connect } from "react-redux";
import { Button } from "react-bootstrap";
import DeviceModal from "./components/DeviceModal";
import ApiHelper from "../../util/ApiHelper";
import { BootstrapTable, TableHeaderColumn } from "react-bootstrap-table";
import { GrStatusGoodSmall } from "react-icons/gr";

class DeviceOverview extends Component {
  state = {
    deviceModalOpen: false,
  };

  componentDidMount() {
    ApiHelper.fetchRegisteredDevices().then();
  }

  openAddDevice() {
    this.setState({
      deviceModalOpen: true,
    });
  }

  async addDevice(deviceData) {
    this.setState({ deviceModalOpen: false });
    console.log("addDevice deviceData", deviceData);

    if (!(await ApiHelper.createRegisteredDevice(deviceData))) {
      alert("Error creating new device");
    }
    ApiHelper.fetchRegisteredDevices().then();
  }

  /**
   * @param subscriber  {Subscriber}
   */
  async deleteRegisteredDevice(DeviceName) {
    if (!window.confirm(`Delete device ${DeviceName}?`)) return;

    const result = await ApiHelper.deleteRegisteredDevice(DeviceName);
    ApiHelper.fetchRegisteredDevices().then();
    if (!result) {
      alert("Error deleting device: " + DeviceName);
    }
  }

  render() {
    return (
      <div className="container-fluid">
        <div className="row">
          <div className="col-md-12">
            <div className="card">
              <div className="header subscribers__header">
                <h1>Device Management</h1>
              </div>
              <div className="header subscribers__header">
                <h3>Registered Devices</h3>
                <Button
                  bsStyle={"primary"}
                  className="subscribers__button"
                  onClick={this.openAddDevice.bind(this)}
                >
                  New Device
                </Button>
              </div>
              <div
                className="content subscribers__content"
                style={{ "overflow-y": "scroll", height: "600px" }}
              >
                {!this.props.get_devices_err && (
                  <BootstrapTable
                    data={this.props.devices}
                    striped={true}
                    hover={true}
                  >
                    <TableHeaderColumn
                      dataField="DeviceID"
                      width="17%"
                      isKey={true}
                      dataAlign="center"
                      dataSort={true}
                    >
                      Device ID
                    </TableHeaderColumn>
                    <TableHeaderColumn
                      dataField="DeviceName"
                      width="17%"
                      dataAlign="center"
                      dataSort={true}
                    >
                      Device Name
                    </TableHeaderColumn>
                    <TableHeaderColumn
                      dataField="Secret"
                      width="17%"
                      dataAlign="center"
                      dataSort={true}
                    >
                      Secret
                    </TableHeaderColumn>
                    <TableHeaderColumn
                      dataField="StaticIP"
                      width="17%"
                      dataAlign="center"
                      dataSort={true}
                    >
                      Static IP
                    </TableHeaderColumn>
                    <TableHeaderColumn
                      dataField="Status"
                      width="17%"
                      dataAlign="center"
                      dataSort={true}
                      dataFormat={(cell, row, rowIndex, formatExtraData) => {
                        if (cell == true) {
                          return (
                            <GrStatusGoodSmall size="1.5em" color="#56f000" />
                          );
                        } else {
                          return (
                            <GrStatusGoodSmall size="1.5em" color="#ff3838" />
                          );
                        }
                      }}
                    >
                      Status
                    </TableHeaderColumn>
                    <TableHeaderColumn
                      dataField="DeviceName"
                      width="15%"
                      dataAlign="center"f
                      dataFormat={(cell, row, rowIndex, formatExtraData) => {
                        return (
                          <Button
                            bsClass="btn-danger"
                            onClick={this.deleteRegisteredDevice.bind(
                              this,
                              cell
                            )}
                          >
                            Delete
                          </Button>
                        );
                      }}
                    >
                      Operation
                    </TableHeaderColumn>
                  </BootstrapTable>
                )}
                {this.props.get_devices_err && (
                  <h2>{this.props.devices_err_msg}</h2>
                )}
              </div>
            </div>
          </div>
        </div>

        <DeviceModal
          open={this.state.deviceModalOpen}
          setOpen={(val) => this.setState({ deviceModalOpen: val })}
          onSubmit={this.addDevice.bind(this)}
        />
      </div>
    );
  }
}

const mapStateToProps = (state) => ({
  subscribers: state.subscriber.subscribers,
  devices: state.registered.devices,
  get_devices_err: state.registered.get_devices_err,
  devices_err_msg: state.registered.devices_err_msg,
});

export default withRouter(connect(mapStateToProps)(DeviceOverview));
