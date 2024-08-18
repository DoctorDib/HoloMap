import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { Provider } from 'react-redux';

import './index.scss';
import App from './App';
import { getStore } from './Stores/store';

import Config from './Common/Config';

ReactDOM.createRoot(document.getElementById('header-root')).render(
    <>
        <title> CAHSI - v{ Config.version } </title>
        <meta name="description" content={'CAHSI - v' + Config.version} />
    </>,
);

ReactDOM.createRoot(document.getElementById('root')).render(
    <BrowserRouter>
        <Provider store={getStore()}> 
            <App />
        </Provider>
    </BrowserRouter>,  
);