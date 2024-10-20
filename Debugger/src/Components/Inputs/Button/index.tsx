import { MouseEventHandler } from 'react';

import './button_style.scss';
import classNames from 'classnames';
import useSound from 'use-sound';

interface ButtonComponentInterface {
    Text?: string | boolean | number | React.ReactElement,
    OnClick: MouseEventHandler<HTMLButtonElement> | any,
    Icon?: React.ReactElement,
    Disabled?: boolean,
    ClassName?: any,
    CustomStyle?: any,
    Sound?: string,
    Mute?: boolean,
}

const ButtonComponent = ({ Text, OnClick, Icon, Disabled, ClassName, CustomStyle, Sound, Mute = false }: ButtonComponentInterface) => {
    const defaultSound = process.env.PUBLIC_URL + '/Sounds/beep.wav';
    const [play] = useSound(Sound == null ? defaultSound : '');
    
    const onClick = () => {
        if (!Mute)
            play();

        OnClick();
    };

    return (
        <button type="button" className={classNames(['button', ClassName])} 
            style={CustomStyle}
            onClick={onClick} disabled={Disabled}>
            {Icon} {Text}
        </button>
    );
};

export default ButtonComponent;