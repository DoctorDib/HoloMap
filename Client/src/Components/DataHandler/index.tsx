import { forwardRef, useImperativeHandle, useState } from 'react';
import { useDispatch } from 'react-redux';

import SpinnerComponent from '../Spinner';

const DataHandlerComponent = forwardRef((_: any, ref: any): React.ReactElement => {
    const dispatch = useDispatch();

    const [spinnerVis, setSpinnerVis] = useState<boolean>(false);
    const [spinnerText, setSpinnerText] = useState<string>('');

    useImperativeHandle(ref, () => ({
        load: async (requestFunc: (data:any) => any, showSpinner = true, data: any = null) => {
            if (showSpinner) {
                setSpinnerText('Loading...');
                setSpinnerVis(true);
            }
            
            await dispatch(requestFunc(data)).catch((_error: Error) => {
                setSpinnerVis(false);
                console.log(`${_error.name}: ${_error.message}`);
            });

            setSpinnerVis(false);
        },
    }));

    return <SpinnerComponent IsVis={spinnerVis} Text={spinnerText} />;
});

DataHandlerComponent.displayName = 'DataHandlerComponent';
export default DataHandlerComponent;