export default class onlineActions {
  static SET_ONLINE_DEVICE = 'ONLINE/SET_ONLINE_DEVICE'
  static SET_ONLINE_DEVICE_ERR = 'ONLINE/SET_ONLINE_DEVICE_ERR'
  static SET_UNIT = 'ONLINE/SET_UNIT'
  static SET_UNIT_ERR = 'ONLINE/SET_UNIT_ERR'

  static setOnlineDevice(devices) {
    return {
      type: this.SET_ONLINE_DEVICE,
      devices: devices,
    };
  }

  static setOnlineDeviceError(errMsg) {
    return {
      type: this.SET_ONLINE_DEVICE_ERR,
      get_devices_err: true,
      devices_err_msg: errMsg
    };
  }

  static setUnit(units) {
    return {
      type: this.SET_UNIT,
      units: units,
    };
  }

  static setUnitError(errMsg) {
    return {
      type: this.SET_UNIT_ERR,
      get_unit_err: true,
      unit_err_msg: errMsg
    };
  }

}
