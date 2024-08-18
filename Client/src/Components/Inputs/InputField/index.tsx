import { useEffect, useState } from 'react';
import Config from '../../../Common/Config';

import './input_field_style.scss';
import '../global-inputs-style.scss';
import classNames from 'classnames';

interface InputFieldComponentInterface {
    Placeholder: string,
    OnEnter?: (input: string)=>void,
    UseShortcut?: boolean,
    Value: string,
    OnChange: (key: string | number, value: string | number)=>void,
    ID?: string | number,
    Disabled?: boolean,
    Type?: string,
    StyleClass?: string,
}

const InputFieldComponent = ({ Placeholder, OnEnter, UseShortcut, Value, OnChange, ID, 
    Disabled, Type, StyleClass }: InputFieldComponentInterface): React.ReactElement => {

    const [text, setText] = useState<string>();
    const [historyIndex, setHistoryIndex] = useState<number>(0);
    const [history, setHistory] = useState<Array<string>>([]);

    const onChange = (value: string): void => {
        if (value.includes(','))
            return;

        OnChange(ID, value);
        setText(value);
    };

    const changeHistoryIndex = (toAdd: number): void => {
        let newIndex: number = historyIndex + toAdd;

        if (newIndex <= 0) {
            newIndex = 0;
        } else if (newIndex + 1 > history.length) {
            newIndex = history.length - 1;
        } else if (newIndex + 1 >= Config.cmd_console.max_history) {
            newIndex = Config.cmd_console.max_history;
        }

        onChange(history[newIndex]);
        setHistoryIndex(newIndex);
    };

    const onEnterPress = (newText: string): void => {
        console.log('Pressed enter');

        if (newText !== '') {
            const newHistory: Array<string> = [...history];
            newHistory.splice(0, 0, newText);
    
            if (newHistory.length > Config.cmd_console.max_history) {
                newHistory.pop();
            }
    
            setHistory(newHistory);
        }

        setText('');
        OnEnter(newText);
    };

    const onKeyPress = (e: any): void => {
        console.log(e.key);
        if (!UseShortcut)
            return;

        switch (e.key) {
            case 'Enter':
            case ',':
                if (text !== '') {
                    onEnterPress(text);
                }
                break;
            case 'ArrowUp':
                changeHistoryIndex(1);
                break;
            case 'ArrowDown':
                changeHistoryIndex(-1);
                break;
        }
    };
    
    useEffect((): void => setText(Value), [Value]);

    return (
        <input 
            type={Type} 
            value={text}
            autoComplete="on"
            disabled={Disabled}
            className={classNames(['input-field', StyleClass])}
            placeholder={Placeholder ?? 'Enter Here...'} 
            onKeyDown={onKeyPress}
            onChange={e => onChange(e.target.value)} 
        />
    );
};

export default InputFieldComponent;