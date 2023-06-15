import React from 'react';
import {Route} from 'react-router-dom';
import UnitOverview from "./UnitOverview";

const UnitManagement = ({match}) => (
  //console.log("In Subscribers")
  <div className="content">
    <Route exact path={`${match.url}/`} component={UnitOverview} />
    {/*<Route path={`${match.url}/:uuid`} component={} />*/}
  </div>
);

export default UnitManagement;
