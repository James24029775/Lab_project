export default class RegisteredDevice {
  DeviceID = "";
  DeviceName = "";
  Secret = "";
  StaticIP = "";
  Status = false;

  constructor(DeviceID, DeviceName, Secret, StaticIP, Status) {
    this.DeviceID = DeviceID;
    this.DeviceName = DeviceName;
    this.Secret = Secret;
    this.StaticIP = StaticIP;
    this.Status = Status;
  }
}
