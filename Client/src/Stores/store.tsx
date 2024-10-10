import { thunk } from 'redux-thunk';
import { createStore, applyMiddleware, combineReducers } from 'redux';

import rootReducer from '../DataHandler/Root/Reducer';
import notificationReducer from '../DataHandler/Notifications/Reducer';
import calibrationReducer from '../DataHandler/Calibration/Reducer';

let store: any = null;

const createNewStore = () => {
    store = createStore(
        combineReducers({
            root: rootReducer,
            notification: notificationReducer,
            calibrations: calibrationReducer,
        }),
        applyMiddleware(thunk),
    );

    return store;
};

const getStore = () => store ?? createNewStore();
export { getStore };