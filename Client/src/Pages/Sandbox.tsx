import React, { useEffect } from 'react';

import '../App.scss';

import { Layer, Projection, useProjection } from 'react-projection-mapping';
import Spotlight from '../Components/QR/Spotlight';

const SandboxPage = (): React.ReactElement => {
    // const [items, setItems] = React.useState({});

    const update = ({ values, action }: any) => {
        // if (action === 'onEnd') {


        console.log(values);

        localStorage.setItem('projection', JSON.stringify(values));

        console.log(action);
        console.log(localStorage);
        // }
    };

    const {
        // data,
        // edit,
        // enabled,
        selectedCorner,
        // selectedLayer,
        // setSelectedCorner,
        // setSelectedLayer,
    } = useProjection();

    // const [items, setItems] = useState();

    // useEffect(() => {
    //     const storage = localStorage.getItem('projection');
    //     if (storage === 'undefined')
    //         return;
        
    //     console.log(localStorage.getItem('projection'));
    //     const bo = JSON.parse(localStorage.getItem('projection'));
    //     if (bo) {
    //         setItems(bo);
    //     }
    // }, []);

    useEffect(() => {
        console.log(selectedCorner);
    }, [selectedCorner]);

    
    return (<>
        <div style={{ background: 'black', width:'1920', height:'100vh' }} >
            
            <Projection onChange={ update } edit={ true } enabled={ true }>
                <Layer id='total'>
                    <div style={{ width:'100%', height:'100%', display: 'flex', justifyContent: 'center', alignItems: 'center', border: '2px solid #0096FF' }}>
                        
                        <Spotlight/>

                    </div>
                </Layer>;
            
            </Projection>
        </div>
    </>);
};

export default SandboxPage;