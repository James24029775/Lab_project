package WebUI

type Tenant struct {
	MissionId         string `json:"missionId"`
	MissionName       string `json:"missionName"`
	// MissionCoordinate string `json:"missionCoordinate"`
	MYSELF_Longitude string `json:"MYSELF_Longitude"`
	MYSELF_Latitude string `json:"MYSELF_Latitude"`
}
