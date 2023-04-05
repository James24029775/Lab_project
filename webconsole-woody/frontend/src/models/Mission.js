import Serializable from "./Serializable";

// export default class Tenant extends Serializable{
//   id = '';
//   name = "";
//   coor = "";


//   constructor(id, name, coor) {
//     super();
//     this.id = id;
//     this.name = name;
//     this.coor = coor;
//   }
// }
export default class Mission extends Serializable{
  missionId = '';
  missionName = "";
  // missionCoordinate = "";
  MYSELF_Longitude = "";
  MYSELF_Latitude = "";
  


  constructor(missionId, missionName, MYSELF_Longitude, MYSELF_Latitude) {
    super();
    this.missionId = missionId;
    this.missionName = missionName;
    // this.missionCoordinate = missionCoordinate;
    this.MYSELF_Longitude = MYSELF_Longitude;
    this.MYSELF_Latitude = MYSELF_Latitude;
  }
}
