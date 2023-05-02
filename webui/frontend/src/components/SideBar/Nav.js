import React, {Component} from 'react';
import {Link, withRouter} from 'react-router-dom';
import LocalStorageHelper from "../../util/LocalStorageHelper";

class Nav extends Component {
  state = {};

  render() {
    let {location} = this.props;
    let user = LocalStorageHelper.getUserInfo();
    let childView = "";
    // if (user.accessToken === "admin") {
    //   childView = (
    //       <li className={this.isPathActive('/tenants') ? 'active' : null}>
    //       <Link to="/tenants">
    //       <i className="pe-7s-users"/>
    //       <p>Tenant and User</p>
    //       </Link>
    //       </li>
    //   );
    // }

    // /* Icons:
    //  *  - https://fontawesome.com/icons
    //  *  - http://themes-pixeden.com/font-demos/7-stroke/
    //  */
    return (
      <ul className="nav">
        <li className={location.pathname === '/' ? 'active' : null}>
          <Link to="/">
            <i className="pe-7s-network"/>
            <p>Realtime Status</p>
          </Link>
        </li>

        <li className={this.isPathActive('/mission') ? 'active' : null}>
          <Link to="/mission">
            <i className="pe-7s-star"/>
            <p>Missions </p>
          </Link>
        </li>

        {/* <li className={this.isPathActive('/registered-ue-page') ? 'active' : null}>
          <Link to="/registered-ue-page">
            <i className="pe-7s-star"/>
            <p>Missions </p>
          </Link>
        </li> */}

      {childView}

      </ul>
    );
  }

  isPathActive(path) {
    return this.props.location.pathname.startsWith(path);
  }
}

export default withRouter(Nav);
