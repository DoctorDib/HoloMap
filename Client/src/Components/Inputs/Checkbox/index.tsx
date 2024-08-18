import React, { useEffect, useState } from 'react';

import './checkbox_style.scss';

interface CheckboxComponentInterface {
    Value: boolean,
    OnChange: (key: string, value: boolean) => void,
    ID: string,
    Disabled: boolean,
}

const CheckBoxComponent = ({ Value, OnChange, ID, Disabled }: CheckboxComponentInterface): React.ReactElement => {
    const [checked, setChecked] = useState<boolean>(false);
    
    const onChange = (value: boolean): void => {
        OnChange(ID, value);
        setChecked(value);
    };

    useEffect((): void => setChecked(Value), [Value]);

    return (
        <div className={'input-container'}>
            <input 
                type="checkbox" 
                checked={checked}
                disabled={Disabled}
                className={'checkbox'}
                onChange={e => onChange(e.target.checked)} 
            />
        </div>
    );
};

export default CheckBoxComponent;