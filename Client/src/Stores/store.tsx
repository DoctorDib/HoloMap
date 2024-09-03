import thunkMiddleware from 'redux-thunk';
import { createStore, applyMiddleware, combineReducers } from 'redux';

import rootReducer from '../DataHandler/Root/Reducer';
import calibrationReducer from '../DataHandler/Calibration/Reducer';

let store: any = null;

const createNewStore = () => {
    store = createStore(
        combineReducers({
            root: rootReducer,
            calibrations: calibrationReducer,
        }),
        applyMiddleware(thunkMiddleware),
    );

    return store;
};

const getStore = () => store ?? createNewStore();
export { getStore };