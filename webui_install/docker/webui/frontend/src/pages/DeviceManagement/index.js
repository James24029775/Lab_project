import React from 'react';
import {Route} from 'react-router-dom';
import DeviceOverview from "./DeviceOverview";

const DeviceManagement = ({match}) => (
  //console.log("In Subscribers")
  <div className="content">
    <Route exact path={`${match.url}/`} component={DeviceOverview} />
    {/*<Route path={`${match.url}/:uuid`} component={} />*/}
  </div>
);

export default DeviceManagement;