import React from "react";
import { Route, withRouter } from "react-router-dom";
import { connect } from "react-redux";
import cx from "classnames";
import { setMobileNavVisibility } from "../../redux/reducers/layout";

import Header from "./Header";
import Footer from "./Footer";
import SideBar from "../../components/SideBar";
/**
 * Pages
 */

import RealtimeStatus from "../RealtimeStatus";
import DeviceManagement from "../DeviceManagement";
import UnitManagement from "../UnitManagement";
import Missions from "../Missions";

const Main = ({
                mobileNavVisibility,
                hideMobileMenu,
                isLoggedIn,
                history
              }) => {
  if (!isLoggedIn) {
    return null;
  }

  history.listen(() => {
    if (mobileNavVisibility === true) {
      hideMobileMenu();
    }
  });

  return (
    <div className={cx({
      "nav-open": mobileNavVisibility === true
    })}>
      <div className="wrapper">
        <div className="close-layer" onClick={hideMobileMenu}/>
        <SideBar/>

        <div className="main-panel">
          <Header/>
          <Route exact path="/" component={RealtimeStatus} />
          <Route exact path="/realtime_status" component={RealtimeStatus} />
          <Route exact path="/device_management" component={DeviceManagement} />
          <Route exact path="/unit_management" component={UnitManagement} />
          <Route exact path="/mission" component={Missions}/>
          <Footer/>
        </div>
      </div>
    </div>
  )
};

const mapStateToProp = state => ({
  mobileNavVisibility: state.layout.mobileNavVisibility
});

const mapDispatchToProps = (dispatch, ownProps) => ({
  hideMobileMenu: () => dispatch(setMobileNavVisibility(false))
});

export default withRouter(connect(mapStateToProp, mapDispatchToProps)(Main));
