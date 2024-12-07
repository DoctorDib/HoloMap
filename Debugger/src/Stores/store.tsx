import { thunk } from 'redux-thunk';
import { applyMiddleware, combineReducers } from 'redux';
import { legacy_createStore as createStore } from 'redux';

import rootReducer from '../DataHandler/Root/Reducer';
import notificationReducer from '../DataHandler/Notifications/Reducer';

let store: any = null;

const createNewStore = () => {
    store = createStore(
        combineReducers({
            root: rootReducer,
            notification: notificationReducer,
        }),
        applyMiddleware(thunk),
    );

    console.log(store);

    return store;
};

const getStore = () => store ?? createNewStore();
export { getStore };