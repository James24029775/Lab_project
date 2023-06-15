import actions from '../actions/onlineActions';

const initialState = {
    devices: [],
    get_devices_err: false,
    devices_err_msg: "",

    units: [],
    get_unit_err: false,
    unit_err_msg: '',
  };

export default function reducer(state = initialState, action) {
let nextState = {...state};

switch (action.type) {       
    case actions.SET_ONLINE_DEVICE:
      nextState.devices = action.devices;
      return nextState;

    case actions.SET_ONLINE_DEVICE_ERR:
      nextState.get_devices_err = action.get_devices_err;
      nextState.devices_err_msg = action.devices_err_msg;
      return nextState;

    case actions.SET_UNIT:
        nextState.units = action.units;
        return nextState;
            
    case actions.SET_UNIT_ERR:
        nextState.get_unit_err = action.get_unit_err
        nextState.unit_err_msg = action.unit_err_msg
        return nextState;
    default:
    return state;
}
};
