import {reducer as formReducer} from 'redux-form'
import auth from './auth';
import layout from './layout';
import subscriber from "./subscriber";
import online from "./online";
import ueinfo from "./ueinfo";
// import tenant from "./tenant";
import user from "./user";
import mission from "./mission"
import registered from "./registered";

export default {
  auth,
  layout,
  subscriber,
  online,
  ueinfo,
  user,
  mission,
  registered,
  // tenant,
  form: formReducer,
};
