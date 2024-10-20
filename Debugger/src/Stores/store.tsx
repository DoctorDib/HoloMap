import { thunk } from 'redux-thunk';
import { createStore, applyMiddleware, combineReducers } from 'redux';

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