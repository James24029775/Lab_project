export default class registeredActions {
  static SET_REGISTERED_DEVICE = "REGISTERED/SET_REGISTERED_DEVICE";
  static SET_REGISTERED_DEVICE_ERR = "REGISTERED/SET_REGISTERED_DEVICE_ERR";
  static SET_REGISTERED_UNIT = "REGISTERED/SET_REGISTERED_UNIT";
  static SET_REGISTERED_UNIT_ERR = "REGISTERED/SET_REGISTERED_UNIT_ERR";

  static setRegisteredDevice(devices) {
    return {
      type: this.SET_REGISTERED_DEVICE,
      devices: devices,
    };
  }

  static setRegisteredDeviceError(errMsg) {
    return {
      type: this.SET_REGISTERED_DEVICE_ERR,
      get_devices_err: true,
      devices_err_msg: errMsg,
    };
  }

  static setRegisteredUnit(units) {
    return {
      type: this.SET_REGISTERED_UNIT,
      units: units,
    };
  }

  static setRegisteredUnitError(errMsg) {
    return {
      type: this.SET_REGISTERED_UNIT_ERR,
      get_unit_err: true,
      unit_err_msg: errMsg
    };
  }
}
