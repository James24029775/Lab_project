import React, { Component } from "react";
import { Modal, Table, Checkbox, Button } from "react-bootstrap";
// import Form from "react-jsonschema-form";
import PropTypes from "prop-types";
import _ from "lodash";
import ApiHelper from "../../../util/ApiHelper";
import { BootstrapTable, TableHeaderColumn } from "react-bootstrap-table";
import { connect } from "react-redux";
import { withRouter } from "react-router-dom";
import OnlineApiHelper from "../../../util/OnlineApiHelper";

class DeviceModal extends Component {
  constructor(props) {
    super(props);

    OnlineApiHelper.fetchOnlineDevice().then();
    ApiHelper.fetchRegisteredDevices().then();

    // this.schema.properties.quota.default = ApiHelper.fetchQuota();
    console.log("constructor");
    this.selectMap = new Map();
  }

  static propTypes = {
    open: PropTypes.bool.isRequired,
    setOpen: PropTypes.func.isRequired,
    onModify: PropTypes.func.isRequired,
    onSubmit: PropTypes.func.isRequired,
    unit: PropTypes.string.isRequired,
    unselectable: PropTypes.array.isRequired,
    selected: PropTypes.array.isRequired,
  };

  state = {
    formData: undefined,
    editMode: false,
    selectRowProp: {
      mode: "checkbox",
      clickToSelect: true,
      unselectable: ["d1", "d3"],
    },
  };

  // async componentDidUpdate(prevProps, prevState, snapshot) {
  //   let quota_temp = await ApiHelper.fetchQuota()["quota"]
  //   console.log("quota in component:", quota_temp)

  //   this.schema.properties.quota.default = quota_temp;
  // }

  componentDidMount() {
    // let arr = this.props.alldevice
    // let selectRow = {
    //   mode: "checkbox",
    //   clickToSelect: true,
    //   unselectable: [],
    //   selected: [],
    // }
    // arr.forEach(element => {
    //   console("element", element.UnitId)
    //   if (element.UnitId != this.props.unit) {
    //     selectRow.unselectable.push(element.DeviceName)
    //   }
    //   else {
    //     selectRow.selected.push(element.DeviceName)
    //   }
    // });
    // console.log("selectRow", selectRow)
    // this.setState({
    //   selectRowProp: selectRow,
    // });
    //   console.log("componentDidMount", this.props.quota)
    //   if (this.props.quota) {
    //     let formData = {
    //       quota: this.props.quota['quota'],
    //     };
    //     this.setState({
    //           formData: formData,
    //     });
    //   }
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    if (prevProps !== this.props) {
      // console.log("Update prevProps", prevProps);
      // console.log("Update props", this.props);
    }

    if (prevProps.open == false && this.props.open) {
      this.selectMap.clear();
      console.log("Update selectMap", this.selectMap);
    }
    // this.props.alldevice
    // if (prevProps !== this.props) {
    //   // this.setState({ editMode: !!this.props.quota });
    //   if (this.props.alldevice) {
    //     let formData = {
    //       alldevice: this.props.alldevice,
    //     };
    //     this.setState({
    //       formData: formData,
    //     });
    //   }
    // }
  }

  async onChange(data) {
    console.log("onChange");

    this.setState({
      formData: data.formData,
    });
  }

  // async updateFormData(newData) {
  //   console.log("updateFormData")

  //   // Workaround for bug: https://github.com/rjsf-team/react-jsonschema-form/issues/758
  //   await this.setState({ rerenderCounter: this.state.rerenderCounter + 1 });
  //   // await this.setState({
  //   //   rerenderCounter: this.state.rerenderCounter + 1,
  //   //   formData: newData,
  //   // });
  // }

  onSubmitClick(result) {
    // console.log("onSubmitClick")

    this.props.onModify(this.selectMap, this.props.unit);
  }

  handleRowSelect(row, isSelected, e) {
    if (this.selectMap.has(row.DeviceName))
      this.selectMap.delete(row.DeviceName);
    else this.selectMap.set(row.DeviceName, isSelected);
  }

  onSelectAll(isSelected, rows) {
    rows.forEach((row) => {
      if (this.selectMap.has(row.DeviceName))
        this.selectMap.delete(row.DeviceName);
      else this.selectMap.set(row.DeviceName, isSelected);
    });
  }

  render() {
    return (
      <Modal
        show={this.props.open}
        className={"fields__edit-modal theme-light"}
        backdrop={"static"}
        onHide={this.props.setOpen.bind(this, false)}
      >
        <Modal.Header closeButton>
          <Modal.Title id="example-modal-sizes-title-lg">
            Device of {this.props.unit}
          </Modal.Title>
        </Modal.Header>

        <Modal.Body>
          {
            // <Form
            //   schema={this.schema}
            //   formData={this.state.formData}
            //   onChange={this.onChange.bind(this)}
            //   onSubmit={this.onSubmitClick.bind(this)}
            // />

            <BootstrapTable
              data={this.props.alldevice}
              striped={true}
              hover={true}
              selectRow={{
                mode: "checkbox",
                clickToSelect: true,
                unselectable: this.props.unselectable,
                selected: this.props.selected,
                onSelect: this.handleRowSelect.bind(this),
                onSelectAll: this.onSelectAll.bind(this),
              }}
            >
              <TableHeaderColumn
                dataField="DeviceName"
                width="40%"
                isKey={true}
                dataAlign="center"
                dataSort={true}
              >
                device Name
              </TableHeaderColumn>
              <TableHeaderColumn
                dataField="StaticIP"
                width="40%"
                dataAlign="center"
                dataSort={true}
              >
                IP
              </TableHeaderColumn>
            </BootstrapTable>

            // <Table
            //   className="subscribers__table"
            //   striped
            //   bordered
            //   condensed
            //   hover
            // >
            //   <thead>
            //     <tr>
            //       <th>Select</th>
            //       <th>Device Name</th>
            //       <th>IP</th>
            //     </tr>
            //   </thead>
            //   <tbody>
            //     <tr>
            //       <td>
            //         <Checkbox />
            //       </td>
            //       <td>d1</td>
            //       <td>192</td>
            //     </tr>
            //     {/* {this.props.tableData.map((subscriber) => (
            //       <tr key={subscriber.deviceName}>
            //         <td>{subscriber.deviceName}</td>
            //         <td>{subscriber.IP}</td>
            //       </tr>
            //     ))} */}
            //   </tbody>
            // </Table>
          }
          {<Button onClick={this.onSubmitClick.bind(this)}>Submit</Button>}
        </Modal.Body>
      </Modal>
    );
  }
}

// export default DeviceModal;

const mapStateToProps = (state) => ({
  subscribers: state.subscriber.subscribers,
  units: state.registered.units,
  get_unit_err: state.registered.get_unit_err,
  unit_err_msg: state.registered.unit_err_msg,
  alldevice: state.registered.devices,
});

export default withRouter(connect(mapStateToProps)(DeviceModal));
