import Http from './Http';
import {store} from '../index';
import subscriberActions from "../redux/actions/subscriberActions";
import Subscriber from "../models/Subscriber";
import missionActions from "../redux/actions/missionActions";
import Mission from "../models/Mission";
import userActions from "../redux/actions/userActions";
import User from "../models/User";
import axios from 'axios';
import LocalStorageHelper from "./LocalStorageHelper";
import RegisteredDevice from "../models/RegisteredDevice";
import registeredActions from "../redux/actions/registeredActions";
import RegisteredUnit from "../models/RegisteredUnit";


class ApiHelper {

  // static async fetchSubscribers() {
  //   try {
  //     let user = LocalStorageHelper.getUserInfo();
  //     axios.defaults.headers.common['Token'] = user.accessToken;
  //     let response = await Http.get('subscriber');
  //     if (response.status === 200 && response.data) {
  //       const subscribers = response.data.map(val => new Subscriber(val['ueId'], val['plmnID']));
  //       store.dispatch(subscriberActions.setSubscribers(subscribers));
  //       return true;
  //     }
  //   } catch (error) {
  //   }

  //   return false;
  // }

  // static async fetchSubscriberById(id, plmn) {
  //   try {
  //     let response = await Http.get(`subscriber/${id}/${plmn}`);
  //     if (response.status === 200 && response.data) {
  //       return response.data;
  //     }
  //   } catch (error) {
  //   }

  //   return false;
  // }

  // static async createSubscriber(subscriberData) {
  //   try {
  //     let user = LocalStorageHelper.getUserInfo();
  //     axios.defaults.headers.common['Token'] = user.accessToken;
  //     let response = await Http.post(
  //       `subscriber/${subscriberData["ueId"]}/${subscriberData["plmnID"]}`, subscriberData);
  //     if (response.status === 201)
  //       return true;
  //   } catch (error) {
  //     console.error(error);
  //   }

  //   return false;
  // }

  // static async updateSubscriber(subscriberData) {
  //   try {
  //     let response = await Http.put(
  //       `subscriber/${subscriberData["ueId"]}/${subscriberData["plmnID"]}`, subscriberData);
  //     if (response.status === 204)
  //       return true;
  //   } catch (error) {
  //     console.error(error);
  //   }

  //   return false;
  // }

  // static async deleteSubscriber(id, plmn) {
  //   try {
  //     let response = await Http.delete(`subscriber/${id}/${plmn}`);
  //     if (response.status === 204)
  //       return true;
  //   } catch (error) {
  //     console.error(error);
  //   }

  //   return false;
  // }

  static async login(loginRequest) {
    console.log("login");
    try {
      let response = await Http.post(`login`, loginRequest);
      return response;
    } catch (error) {
      console.error(error);
    }
    return false;
  }

  // Missions
  static async fetchMissions() {
    try {
      store.dispatch(missionActions.setMissions([]));
      let user = LocalStorageHelper.getUserInfo();
      axios.defaults.headers.common['Token'] = user.accessToken;
      let response = await Http.get('mission/getmission');
      if (response.status === 200 && response.data) {
        const missions = response.data.map(val => new Mission(val['missionId'], val['missionName'], val['MYSELF_Longitude'], val['MYSELF_Latitude']));
        console.log(missions);
        store.dispatch(missionActions.setMissions(missions));
        return true;
      }
    } catch (error) {
    }

    return false;
  }

  static async fetchTheNewestMission() {
    try {
      let user = LocalStorageHelper.getUserInfo();
      axios.defaults.headers.common['Token'] = user.accessToken;
      let response = await Http.get(`mission/getmission`);
      if (response.status === 200 && response.data) {
        return response.data;
      }
    } catch (error) {
    }
    return false;
  }

  static async fetchMissionById(id) {
    try {
      let user = LocalStorageHelper.getUserInfo();
      axios.defaults.headers.common['Token'] = user.accessToken;
      let response = await Http.get(`mission/fetch/${id}`);
      if (response.status === 200 && response.data) {
        return response.data;
      }
    } catch (error) {
    }

    return false;
  }

  static async createMission(missionData) {
    try {
      console.log("check point 1");
      let user = LocalStorageHelper.getUserInfo();
      console.log("check point 2");
      axios.defaults.headers.common['Token'] = user.accessToken;
      console.log("check point 3");
      let response = await Http.post('mission/createmission', missionData);
      console.log("check point 4");

      if (response.status === 200)
        return true;
    } catch (error) {
      console.error(error);
    }

    return false;
  }

  static async updateMission(missionData) {
    try {
      let user = LocalStorageHelper.getUserInfo();
      axios.defaults.headers.common['Token'] = user.accessToken;
      let response = await Http.put(
        `mission/update/${missionData["missionId"]}`, missionData);
      if (response.status === 200)
        return true;
    } catch (error) {
      console.error(error);
    }

    return false;
  }

  static async deleteMission(id) {
    try {
      let user = LocalStorageHelper.getUserInfo();
      axios.defaults.headers.common['Token'] = user.accessToken;
      let response = await Http.delete(`mission/delete/${id}`);
      if (response.status === 200)
        return true;
    } catch (error) {
      console.error(error);
    }

    return false;
  }

  
  // Registered User Equipment
  static async fetchRegisteredDevices() {
    const MSG_FETCH_ERROR = "Error fetching registered devices.";

    try {
      let response = await Http.get("device/getdevice");
      if (response.status === 200 && response.data.devices) {
        const devices = response.data.devices.map(
          (val) =>
            new RegisteredDevice(
              val["deviceId"],
              val["name"],
              val["secret"],
              val["ip"],
              val["status"]
            )
        );
        store.dispatch(registeredActions.setRegisteredDevice(devices));
        return true;
      }
    } catch (error) {
      let err_msg;
      if (error.response && error.response.data) {
        err_msg = error.response.data.cause || MSG_FETCH_ERROR;
      } else {
        err_msg = MSG_FETCH_ERROR;
      }
      console.log(error.response);
      store.dispatch(registeredActions.setRegisteredDeviceError(err_msg));
    }

    return false;
  }


  static async createRegisteredDevice(deviceData) {
    try {
      let user = LocalStorageHelper.getUserInfo();
      axios.defaults.headers.common[
        "Authorization"
      ] = `Bearer ${user.accessToken}`;
      // axios.defaults.headers.common["Token"] = user.accessToken;
      if(deviceData.staticIP == null) deviceData.staticIP = "";
      let response = await Http.post(`device/` + deviceData.deviceName, {
        id: deviceData.deviceID,
        ip: deviceData.staticIP,
        secret: deviceData.secret,
      });
      // ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
      // if (response.status === 201 || response.status === 200) {
      //   let response = await Http.post(
      //     `group/combat/devices/` + deviceData.deviceName
      //   );
      //   return true;
      // }
      // ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
      // return true取代上面
      return true;
    } catch (error) {
      console.error(error);
    }

    return false;
  }

  // ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
  static async addDeviceToUnit(device, unit) {

    try {
      let user = LocalStorageHelper.getUserInfo();
      axios.defaults.headers.common[
        "Authorization"
      ] = `Bearer ${user.accessToken}`;

      console.log(device, unit);
      let response = await Http.post(`device/${device}/join/${unit}`);
      if (response.status === 201 || response.status === 200) {
        return true;
      }
    } catch (error) {
      console.error(error);
    }

    return false;
  }


  static async deleteDeviceFromUnit(device, unit) {
    try {
      let user = LocalStorageHelper.getUserInfo();
      axios.defaults.headers.common[
        "Authorization"
      ] = `Bearer ${user.accessToken}`;
      console.log(`device/${device}/leave/${unit}`);
      let response = await Http.post(`device/${device}/leave/${unit}`);
      if (response.status === 201 || response.status === 200) {
        return true;
      }
    } catch (error) {
      console.error(error);
    }

    return false;
  }


  static async deleteRegisteredDevice(DeviceName) {
    let user = LocalStorageHelper.getUserInfo();
    axios.defaults.headers.common[
      "Authorization"
    ] = `Bearer ${user.accessToken}`;
    // ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
    // let response1 = await Http.delete(`group/combat/devices/${DeviceName}`);
    // ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！

    // try {
    // removeDeviceFromGroup
    // let user = LocalStorageHelper.getUserInfo();
    // axios.defaults.headers.common[
    //   "Authorization"
    // ] = `Bearer ${user.accessToken}`;
    let response2 = await Http.delete(`device/${DeviceName}`);

    if (response2.status === 204 || response2.status === 200) return true;
    // } catch (error) {
    //   console.error(error);
    // }

    return false;
  }


  // static async fetchRegisteredUnits() {
  //   const MSG_FETCH_ERROR = "Error fetching online registered units.";

  //   try {
  //     let response = await Http.get("registered-units");
  //     if (response.status === 200 && response.data) {
  //       const units = response.data.map(
  //         (val) =>
  //           new RegisteredUnit(
  //             val["unitID"],
  //             val["unitName"],
  //             val["bitrateLimit"]
  //           )
  //       );
  //       store.dispatch(registeredActions.setRegisteredUnit(units));
  //       return true;
  //     }
  //   } catch (error) {
  //     let err_msg;
  //     if (error.response && error.response.data) {
  //       err_msg = error.response.data.cause || MSG_FETCH_ERROR;
  //     } else {
  //       err_msg = MSG_FETCH_ERROR;
  //     }
  //     console.log(error.response);
  //     store.dispatch(registeredActions.setRegisteredUnitError(err_msg));
  //   }

  //   return false;
  // }

  static async createRegisteredUnit(unitData) {
    try {
      let user = LocalStorageHelper.getUserInfo();
      axios.defaults.headers.common[
        "Authorization"
      ] = `Bearer ${user.accessToken}`;

      if (unitData.bitrateLimit === "") {
        let response = await Http.post(`group/combat/unit/` + unitData.unitName);
        if (response.status === 201 || response.status === 200) {
          return true;
        }
      } else {
        let response = await Http.post(`group/combat/unit/` + unitData.unitName, {
          bitrateLimit: unitData.bitrateLimit,
        });
        if (response.status === 201 || response.status === 200) {
          return true;
        }
      }
    } catch (error) {
      console.error(error);
    }

    return false;
  }


  static async deleteRegisteredUnit(UnitName) {
    try {
      // removeDeviceFromGroup
      let user = LocalStorageHelper.getUserInfo();
      axios.defaults.headers.common[
        "Authorization"
      ] = `Bearer ${user.accessToken}`;
      let response = await Http.delete(`group/combat/unit/${UnitName}`);

      if (response.status === 204 || response.status === 200) return true;
    } catch (error) {
      console.error(error);
    }

    return false;
  }














  // static async fetchUsers(tenantId) {
  //   try {
  //     store.dispatch(userActions.setUsers([]));
  //     let user = LocalStorageHelper.getUserInfo();
  //     axios.defaults.headers.common['Token'] = user.accessToken;
  //     let response = await Http.get(`tenant/${tenantId}/user`);
  //     if (response.status === 200 && response.data) {
  //       const users = response.data.map(val => new User('', '', '', val['userId'], val['email']));
  //       store.dispatch(userActions.setUsers(users));
  //       return true;
  //     }
  //   } catch (error) {
  //   }

  //   return false;
  // }

  // static async fetchUserById(tenantId, id) {
  //   try {
  //     let user = LocalStorageHelper.getUserInfo();
  //     axios.defaults.headers.common['Token'] = user.accessToken;
  //     let response = await Http.get(`tenant/${tenantId}/user/${id}`);
  //     if (response.status === 200 && response.data) {
  //       return response.data;
  //     }
  //   } catch (error) {
  //   }

  //   return false;
  // }

  // static async createUser(tenantId, userData) {
  //   try {
  //     let user = LocalStorageHelper.getUserInfo();
  //     axios.defaults.headers.common['Token'] = user.accessToken;
  //     userData['encryptedPassword'] = userData['password'];
  //     let response = await Http.post(
  //       `tenant/${tenantId}/user`, userData);
  //     if (response.status === 200)
  //       return true;
  //   } catch (error) {
  //     console.error(error);
  //   }

  //   return false;
  // }

  // static async updateUser(tenantId, userId, userData) {
  //   try {
  //     let user = LocalStorageHelper.getUserInfo();
  //     axios.defaults.headers.common['Token'] = user.accessToken;
  //     userData['encryptedPassword'] = userData['password'];
  //     let response = await Http.put(
  //       `tenant/${tenantId}/user/${userId}`, userData);
  //     if (response.status === 200)
  //       return true;
  //   } catch (error) {
  //     console.error(error);
  //   }

  //   return false;
  // }

  // static async deleteUser(tenantId, id) {
  //   try {
  //     let user = LocalStorageHelper.getUserInfo();
  //     axios.defaults.headers.common['Token'] = user.accessToken;
  //     let response = await Http.delete(`tenant/${tenantId}/user/${id}`);
  //     if (response.status === 200)
  //       return true;
  //   } catch (error) {
  //     console.error(error);
  //   }

  //   return false;
  // }

}

export default ApiHelper;
