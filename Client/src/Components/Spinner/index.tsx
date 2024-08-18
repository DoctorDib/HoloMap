import React from 'react';
import { SpinnerCircularSplit } from 'spinners-react';

import './spinner_style.scss';

interface SpinnerComponentInterface {
    IsVis: boolean,
    Text: string,
}

const SpinnerComponent = ({ IsVis, Text }: SpinnerComponentInterface): React.ReactElement => {
    return <>
        { IsVis && <div className={'spinner-background'}>
            <SpinnerCircularSplit size={50} thickness={100} speed={100} color="#36ad47" secondaryColor="rgba(0, 0, 0, 0.44)" />
            <div className={'spinner-text'}>
                { Text }
            </div>
        </div> }
    </>;
};

export default SpinnerComponent;