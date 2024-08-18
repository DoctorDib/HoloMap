import { useEffect, useRef  } from 'react';
import { Route, Routes } from 'react-router-dom';

import './App.scss';

import Dashboard from './Pages/Dashboard';
import NotFound from './Pages/NotFound';
import DataHandlerComponent from './Components/DataHandler';
import Sandbox from './Pages/Sandbox';
import { initialiseDataRequest } from './DataHandler/Actions/rootActions';

const App = (): React.ReactElement => {
    const dataHandlerRef = useRef(null);
    const landingPageRef = useRef(null);

    useEffect(() => {
        console.log('WAWEOAMSDOALSD<F');
        // Initialising data and sockets
        initialiseDataRequest();
    }, []);

    return (<>
        <div className={'App'}>
            <main className={'content'}>
                <Routes>
                    <Route path='/' element={<Dashboard ref={landingPageRef} />} />
                    <Route path='*' element={<NotFound /> } />
                    <Route path='/sandbox' element={<Sandbox /> } />
                </Routes>
            </main>
        </div>

        <DataHandlerComponent ref={dataHandlerRef} />
    </>);
};

export default App;