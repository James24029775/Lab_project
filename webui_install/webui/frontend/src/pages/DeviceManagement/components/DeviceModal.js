import React, { Component } from "react";
import { Modal } from "react-bootstrap";
import Form from "react-jsonschema-form";
import PropTypes from "prop-types";
import _ from "lodash";

class DeviceModal extends Component {
  static propTypes = {
    open: PropTypes.bool.isRequired,
    setOpen: PropTypes.func.isRequired,
    subscriber: PropTypes.object,
    onModify: PropTypes.func.isRequired,
    onSubmit: PropTypes.func.isRequired,
  };

  state = {
    editMode: false,
    formData: undefined,
    // for force re-rendering json form
    rerenderCounter: 0,
  };

  state = {
    formData: undefined,
    editMode: false,
    // for force re-rendering json form
    rerenderCounter: 0,
  };

  schema = {
    // title: "A registration form",
    // "description": "A simple form example.",
    type: "object",
    required: ["DeviceName", "Secret"],
    properties: {
      DeviceName: {
        type: "string",
        title: "Device Name",
        default: "name",
      },
      Secret: {
        type: "string",
        title: "Secret",
        default: "Secret",
      },

      IP: {
        type: "string",
        title: "IP",
        pattern: "^((25[0-5]|(2[0-4]|1\\d|[1-9]|)\\d).?\\b){4}$",
        default: "192.168.0.0",
      },
    },
  };

  uiSchema = {
    OPOPcSelect: {
      "ui:widget": "select",
    },
    authenticationMethod: {
      "ui:widget": "select",
    },
    SliceConfiurations: {
      "ui:options": {
        orderable: false,
      },
      isDefault: {
        "ui:widget": "radio",
      },
      dnnConfigurations: {
        "ui:options": {
          orderable: false,
        },
        flowRules: {
          "ui:options": {
            orderable: false,
          },
        },
      },
    },
  };

  componentDidUpdate(prevProps, prevState, snapshot) {
    if (prevProps !== this.props) {
      this.setState({ editMode: !!this.props.subscriber });

      if (this.props.subscriber) {
        const subscriber = this.props.subscriber;

        let formData = {
          DeviceID: "0",
          DeviceName: subscriber["DeviceName"],
          Secret: subscriber["Secret"],
          IP: subscriber["IP"],
        };

        this.updateFormData(formData).then();
      }
    }
  }

  async updateFormData(newData) {
    // Workaround for bug: https://github.com/rjsf-team/react-jsonschema-form/issues/758
    await this.setState({ rerenderCounter: this.state.rerenderCounter + 1 });
    await this.setState({
      rerenderCounter: this.state.rerenderCounter + 1,
      formData: newData,
    });
  }

  onSubmitClick(result) {
    const formData = result.formData;

    let subscriberData = {
      deviceID: "0",
      deviceName: formData["DeviceName"],
      secret: formData["Secret"], // Change required
      staticIP: formData["IP"],
    };

    this.props.onSubmit(subscriberData);
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
            {this.state.editMode ? "Edit Subscriber" : "New Device"}
          </Modal.Title>
        </Modal.Header>

        <Modal.Body>
          {this.state.rerenderCounter % 2 === 0 && (
            <Form
              schema={this.schema}
              uiSchema={this.uiSchema}
              formData={this.state.formData}
              onSubmit={this.onSubmitClick.bind(this)}
            />
          )}
        </Modal.Body>
      </Modal>
    );
  }
}

export default DeviceModal;
