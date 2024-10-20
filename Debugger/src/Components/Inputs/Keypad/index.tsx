import React, { useEffect, useState } from 'react';

import Button from '../Button';
import Icons from '../../../Common/Icons';
import InputField from '../InputField';

import './keypad_style.scss';
import useSound from 'use-sound';

interface KeypadComponentInterface {
    Value: string,
    OnChange: (key: string, value: string) => void,
    ID: string,
    Disabled?: boolean,
    OnGoClick: () => void,
    Label: string,
}

const KeypadComponent = ({ Value, OnChange, ID, Disabled, OnGoClick, Label }: KeypadComponentInterface): React.ReactElement => {
    const defaultSound = process.env.PUBLIC_URL + '/Sounds/beep.wav';
    const keypadValues: Array<string> =  '12345X67890>'.split('');
    const [keypad, setKeypad] = useState<string>('');
    const [play] = useSound(defaultSound);

    const onClick = (value: string): void => {
        let newVal: string;
        if (value === 'X') {
            newVal = '';
        } else if (value === '>') {
            OnGoClick();
            return;
        } else {
            newVal = keypad + value;
        }

        setKeypad(newVal);
        OnChange(ID, newVal);
    };

    const onChange = (key: string, value: any): void => {
        play();
        setKeypad(value);
        OnChange(key, value);
    };

    const mapButtons = (): Array<React.ReactElement> => {
        const buttons: Array<React.ReactElement> = [];
        let row: Array<React.ReactElement> = [];
        for (let index = 0; index < keypadValues.length; index++) {
            let stringVal: any = keypadValues[index];
            let icon: any = null;
            if (stringVal === 'X') {
                stringVal = 'CLEAR';
            } else if (stringVal === '>') {
                icon = Icons.Play;
                stringVal = '';
            }
            
            const classKey = stringVal == '<' ? 'delete-key' :
                stringVal == '>' ? 'enter-key' : '';

            row.push(<Button key={index} Text={stringVal} Icon={icon} 
                ClassName={classKey} OnClick={() => onClick(keypadValues[index])} Disabled={Disabled} />);

            if ((index + 1) % 6 === 0) {
                buttons.push(<div key={index} className={'keypad--row'}> { row } </div>);
                row = [];
            }
        }
        return buttons;
    };

    useEffect((): void => { setKeypad(Value ?? ''); }, [Value]);

    return (
        <div className={'keypad--parent'}>
            <InputField StyleClass={'keypad--text'} Type={'password'} ID={ID} Value={keypad}
                OnChange={onChange} Placeholder={Label} OnEnter={() => OnGoClick()} UseShortcut/>
            <div className={'keypad--button-container'}> { mapButtons() } </div>
        </div>
    );
};

export default KeypadComponent;