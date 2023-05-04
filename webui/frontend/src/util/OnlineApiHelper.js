import Http from "./Http";
import { store } from "../index";
import onlineActions from "../redux/actions/onlineActions";
import OnlineDevice from "../models/OnlineDevice";
import OnlineUnit from "../models/OnlineUnit";

class OnlineApiHelper {
  static async fetchOnlineUnit() {
    const MSG_FETCH_ERROR = "Error fetching online units.";

    try {
      let url = "exporter/";

      let response = await Http.get(url);
      if (response.status === 200) {
        let units = [];

        if (response.data.units) {
          console.log("response.data", response.data);

          units = response.data.units.map(
            (unit) => new OnlineUnit(unit.unitId, unit.unitName, unit.bandwidthLimit, unit.members)
          );

          store.dispatch(onlineActions.setUnit(units));
        } else {
          store.dispatch(onlineActions.setUnit(units));
        }
        return true;
      } else {
        console.log("Request failed, url:", url);
        console.log("Response: ", response.status, response.data);

        let err_msg;
        if (response.data !== undefined) {
          err_msg = response.data;
        } else {
          err_msg = MSG_FETCH_ERROR;
        }
        store.dispatch(onlineActions.setUnitError(err_msg));
      }
    } catch (error) {
      let err_msg;
      if (error.response && error.response.data) {
        err_msg = error.response.data.cause || MSG_FETCH_ERROR;
      } else {
        err_msg = MSG_FETCH_ERROR;
      }
      console.log(error.response);
      store.dispatch(onlineActions.setUnitError(err_msg));
    }

    return false;
  }

  static async fetchOnlineDevice() {
    const MSG_FETCH_ERROR = "Error fetching online devices.";

    try {
      let url = "device/getalive";

      let response = await Http.get(url);
      if (response.status === 200) {
        let devices = [];

        if (response.data) {
          // console.log("response.data", response.data)
          devices = response.data.devices.map(
            (device) =>
              new OnlineDevice(
                device.devicename,
                device.ip,
                device.txbitrate,
                device.rssi,
                device.ssid,
                device.bssid
                // device.unitid
              )
          );

          console.log("devices", devices);

          store.dispatch(onlineActions.setOnlineDevice(devices));
        } else {
          store.dispatch(onlineActions.setOnlineDevice(devices));
        }
        return true;
      } else {
        console.log("Request failed, url:", url);
        console.log("Response: ", response.status, response.data);

        let err_msg;
        if (response.data !== undefined) {
          err_msg = response.data;
        } else {
          err_msg = MSG_FETCH_ERROR;
        }
        store.dispatch(onlineActions.setOnlineDeviceError(err_msg));
      }
    } catch (error) {
      let err_msg;
      if (error.response && error.response.data) {
        err_msg = error.response.data.cause || MSG_FETCH_ERROR;
      } else {
        err_msg = MSG_FETCH_ERROR;
      }
      console.log(error.response);
      store.dispatch(onlineActions.setOnlineDeviceError(err_msg));
    }

    return false;
  }
}

export default OnlineApiHelper;
