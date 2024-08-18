import thunkMiddleware from 'redux-thunk';
import { createStore, applyMiddleware, combineReducers } from 'redux';

import rootReducer from '../DataHandler/Reducers/rootReducer';

let store: any = null;

const createNewStore = () => {
    store = createStore(
        combineReducers({
            root: rootReducer,
        }),
        applyMiddleware(thunkMiddleware),
    );

    return store;
};

const getStore = () => store ?? createNewStore();
export { getStore };