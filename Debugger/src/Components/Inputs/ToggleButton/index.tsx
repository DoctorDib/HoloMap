import { MouseEventHandler, useEffect, useState } from 'react';

import './toggle_button_style.scss';
import classNames from 'classnames';

interface ButtonComponentInterface {
    Text?: string | boolean | number | React.ReactElement,
    OnClick: MouseEventHandler<HTMLButtonElement> | any,
    Icon?: React.ReactElement,
    Disabled?: boolean,
    ClassName?: any,
    IsActive?: boolean,
}

const ToggleButtonComponent = ({ Text, OnClick, Icon, Disabled, ClassName, IsActive }: ButtonComponentInterface) => {    
    const [isActive, setIsActive] = useState(false);

    const onClick = () => {
        setIsActive(!isActive);
        // Calling custom function
        OnClick(isActive);
    };

    useEffect(() => {
        if (IsActive !== null && IsActive !== undefined) {
            setIsActive(IsActive);
        }
    }, [IsActive])

    return (
        <button type="button" className={classNames(['toggle-button', ClassName, isActive ? 'toggle-button-active' : ''])} 
            onClick={onClick} disabled={Disabled}>
            {Icon} {Text}
        </button>
    );
};

export default ToggleButtonComponent;