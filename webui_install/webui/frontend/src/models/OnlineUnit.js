class deviceStatus {
  DeviceName = "";
  Status = false;
  TxBitrate = "";
  RSSI = "";

  constructor(DeviceName, Status, TxBitrate, RSSI) {
    this.DeviceName = DeviceName;
    this.Status = Status;
    this.TxBitrate = TxBitrate;
    this.RSSI = RSSI;
  }
}

export default class OnlineUnit {
  UnitId = "";
  UnitName = "";
  BitrateLimit = "";
  Members = [];

  constructor(UnitId, UnitName, BitrateLimit, Members) {
    this.UnitId = UnitId;
    this.UnitName = UnitName;
    this.Members = Members.map(
      (device) =>
        new deviceStatus(
          device.name,
          device.status,
          device.txbitrate,
          device.rssi
        )
    );
    this.BitrateLimit = BitrateLimit;
  }
}
