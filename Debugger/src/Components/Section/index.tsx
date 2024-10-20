import React from 'react';

import './section_style.scss';

interface MasterComponentInterface {
    component: React.ReactNode;
}

const SectionComponent = ({ component }: MasterComponentInterface): React.ReactElement => {
    return <>
        <div className={'section-container'}>
            { component}
        </div>
    </>;
};

export default SectionComponent;