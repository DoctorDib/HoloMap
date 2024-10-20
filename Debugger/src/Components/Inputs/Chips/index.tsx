import React, { useEffect, useState } from 'react';

import './chips_style.scss';

import InputField from '../InputField';

interface ChipsComponentInterface {
    ID: string | number,
    OnChange: (key: string | number, value: any)=>void,
    Data: any,
}

const ChipsComponent = ({ ID, OnChange, Data }: ChipsComponentInterface): React.ReactElement => {
    const [text, setText] = useState<string>();
    const [chips, setChips] = useState<Array<string>>([]);

    const AddChip = (newChip: string): void => {
        setText('');
        const newChips = [...chips, newChip];
        setChips(newChips);
        OnChange(ID, newChips);
    };

    const RemoveChips = (index: number): void => {
        let newChips = [...chips];

        // Removing chip from array
        newChips.splice(index, 1);
        
        // removing undefined from list
        newChips = newChips.filter(element => element !== undefined);

        setChips(newChips);
        OnChange(ID, newChips);
    };

    const OnChipClick = (index: number): void => { 
        RemoveChips(index);
        setText(chips[index]);
    };

    useEffect((): void => setChips(Data), [Data]);

    return <> 
        <div className={'chip-container'}>
            <InputField UseShortcut Type={'text'}
                OnChange={(_:any, value: string) => setText(value)} Value={text} OnEnter={AddChip} Placeholder={'Enter Command...'} />
            <div className={'chip-parent'}>
                { chips.map((chip: string, _index: number): React.ReactElement => (
                    <div className={'chip'} key={_index} onClick={() => OnChipClick(_index)}>
                        { chip }
                    </div>
                )) }
            </div>
        </div>
    </>;
};

export default ChipsComponent;