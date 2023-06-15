import React, { Component } from "react";
import { Button } from "react-bootstrap";
import { withRouter } from "react-router-dom";
import { BootstrapTable, TableHeaderColumn } from "react-bootstrap-table";
import { connect } from "react-redux";
import UEInfoApiHelper from "../../util/OnlineApiHelper";
import { GrStatusGoodSmall } from "react-icons/gr";

class RealtimeStatus extends Component {
  componentDidMount() {
    UEInfoApiHelper.fetchOnlineDevice().then();
    UEInfoApiHelper.fetchOnlineUnit().then();
  }

  refreshTable() {
    UEInfoApiHelper.fetchOnlineDevice().then();
    UEInfoApiHelper.fetchOnlineUnit().then();
  }
  numberOfPicture = [1, 2, 3, 4, 5, 6];

  render() {
    return (
      <div className="container-fluid">
        <div className="row">
          <div className="col-md-12">
            <div className="card" style={{
                  height: "1020px",
                }}>
              <div className="header subscribers__header">
                <h1>Realtime Status</h1>
                <Button
                  bsStyle={"primary"}
                  className="subscribers__button"
                  onClick={this.refreshTable.bind(this)}
                >
                  Refresh
                </Button>
              </div>
              <div className="header subscribers__header">
                <h3>Online Devices</h3>
              </div>
              <div
                className="content subscribers__content"
                style={{ "overflow-y": "scroll", height: "300px" }}
              >
                {!this.props.get_devices_err && (
                  <BootstrapTable
                    data={this.props.devices}
                    striped={true}
                    hover={true}
                  >
                    <TableHeaderColumn
                      dataField="DeviceName"
                      width="15%"
                      isKey={true}
                      dataAlign="center"
                      dataSort={true}
                    >
                      Device Name
                    </TableHeaderColumn>

                    <TableHeaderColumn
                      dataField="IP"
                      width="15%"
                      dataAlign="center"
                      dataSort={true}
                    >
                      IP
                    </TableHeaderColumn>

                    <TableHeaderColumn
                      dataField="TxBitrate"
                      width="15%"
                      dataAlign="center"
                      dataSort={true}
                    >
                      TxBitrate(Mbps)
                    </TableHeaderColumn>

                    <TableHeaderColumn
                      dataField="RSSI"
                      width="15%"
                      dataAlign="center"
                      dataSort={true}
                    >
                      RSSI(dBm)
                    </TableHeaderColumn>

                    <TableHeaderColumn
                      dataField="SSID"
                      width="15%"
                      dataAlign="center"
                      dataSort={true}
                    >
                      SSID
                    </TableHeaderColumn>

                    <TableHeaderColumn
                      dataField="BSSID"
                      width="15%"
                      dataAlign="center"
                      dataSort={true}
                    >
                      BSSID
                    </TableHeaderColumn>

                    {/* <TableHeaderColumn
                      dataField="UnitId"
                      width="20%"
                      dataSort={true}
                    >
                      Unit Id
                    </TableHeaderColumn> */}
                  </BootstrapTable>
                )}
                {this.props.get_devices_err && (
                  <h2>{this.props.devices_err_msg}</h2>
                )}
              </div>

              <div className="header subscribers__header">
                <h3>Online Units</h3>
              </div>

              {/* <div className="header subscribers__header">
                <ScrollMenu
                  arrowLeft={<div style={{ fontSize: "30px" }}>{" < "}</div>}
                  arrowRight={<div style={{ fontSize: "30px" }}>{" > "}</div>}
                  data={this.numberOfPicture.map((picture, index) => (
                    <img
                      style={{ height: "100px" }}
                      alt="test"
                      src="https://reactjs.org/logo-og.png"
                    />
                  ))}
                />
              </div> */}

              <div
                className="content subscribers__content"
                style={{float:"left", "overflow-y": "scroll", height: "500px" }}
              >
                {/* {!this.props.get_unit_err && ( */}
                {this.props.units &&
                  this.props.units.map((unit) => (
                    <div
                      className="card"
                      style={{
                        display: "inline-block",
                        margin: "10px 10px 10px 10px",
                        width: "45%",
                      }}
                    >
                      <h3>&nbsp;Unit:&nbsp;{unit.UnitName}&#40;{unit.UnitId}&#41;</h3>
                      <BootstrapTable
                        data={[unit]}
                        striped={true}
                        hover={true}
                        containerStyle={{
                          margin: "5px 5px 5px 5px",
                        }}
                      >
                        <TableHeaderColumn
                          dataField="UnitId"
                          width="30%"
                          isKey={true}
                          dataAlign="center"
                        >
                          Unit Id
                        </TableHeaderColumn>

                        <TableHeaderColumn
                          dataField="UnitName"
                          width="30%"
                          dataAlign="center"
                        >
                          Unit Name
                        </TableHeaderColumn>

                        <TableHeaderColumn
                          dataField="BitrateLimit"
                          width="30%"
                          dataAlign="center"
                        >
                          Bandwidth Limit
                        </TableHeaderColumn>
                      </BootstrapTable>
                      {/* <p>&nbsp;</p> */}
                      <h4>&nbsp;Device List</h4>
                      <BootstrapTable
                        data={unit.Members}
                        striped={true}
                        hover={true}
                        containerStyle={{
                          margin: "5px 5px 5px 5px",
                        }}
                      >
                        <TableHeaderColumn
                          dataField="DeviceName"
                          width="25%"
                          isKey={true}
                          dataAlign="center"
                          dataSort={true}
                        >
                          Device Name
                        </TableHeaderColumn>

                        <TableHeaderColumn
                          dataField="TxBitrate"
                          width="25%"
                          dataAlign="center"
                          dataSort={true}
                        >
                          TxBitrate (Mbps)
                        </TableHeaderColumn>

                        <TableHeaderColumn
                          dataField="RSSI"
                          width="25%"
                          dataAlign="center"
                          dataSort={true}
                        >
                          RSSI (dBm)
                        </TableHeaderColumn>

                        <TableHeaderColumn
                          dataField="Status"
                          width="25%"
                          dataAlign="center"
                          dataSort={true}
                          dataFormat={(
                            cell,
                            row,
                            rowIndex,
                            formatExtraData
                          ) => {
                            if (cell == true) {
                              return <GrStatusGoodSmall size="1.5em" color="#56f000"/>;
                            }
                            else {
                              return <GrStatusGoodSmall size="1.5em" color="#ff3838"/>;
                            }
                          }}
                        >
                          Status
                        </TableHeaderColumn>
                      </BootstrapTable>
                    </div>
                  ))}

                {/* )} */}
                {/* {this.props.get_unit_err && <h2>{this.props.unit_err_msg}</h2>} */}
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default withRouter(
  connect((state) => ({
    devices: state.online.devices,
    get_devices_err: state.online.get_devices_err,
    devices_err_msg: state.online.devices_err_msg,

    units: state.online.units,
    get_unit_err: state.online.get_unit_err,
    unit_err_msg: state.online.unit_err_msg,
  }))(RealtimeStatus)
);
