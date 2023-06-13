export default class RegisteredDevice {
  UnitID = "";
  UnitName = "";
  BitrateLimit = "";

  constructor(UnitID, UnitName, BitrateLimit) {
    this.UnitID = UnitID;
    this.UnitName = UnitName;
    this.BitrateLimit = BitrateLimit;
  }
}
