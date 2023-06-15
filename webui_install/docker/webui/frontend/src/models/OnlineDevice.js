export default class OnlineDevice {
  DeviceName = "";
	IP          = "";    
	TxBitrate   = "";    
	RSSI        = "";    
  SSID = "";
  BSSID = "";

  constructor(DeviceName, IP, TxBitrate, RSSI, SSID, BSSID) {
    this.DeviceName = DeviceName;
    this.IP = IP;
    this.TxBitrate = TxBitrate;
    this.RSSI = RSSI;
    this.SSID = SSID;
    this.BSSID = BSSID;
  }
}
