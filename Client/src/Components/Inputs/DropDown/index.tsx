import './dropdown_style.scss';
import '../global-inputs-style.scss';
import React, { useEffect, useState } from 'react';
import classNames from 'classnames';

interface DropDownComponentInterface {
    Options: Array<React.ReactElement | string>,
    Value?: string,
    OnChange?: (key: string, value: any)=>void,
    ID?: string,
    StaticOptions?: React.ReactElement,
    Disabled?: boolean,
}

const DropDownComponent = ({ Value, OnChange, ID, Options, StaticOptions = null, Disabled }: DropDownComponentInterface) => {    
    const [elementOptions, setOptions] = useState<React.ReactElement[]>();
    const [selectedOption, setSelectedOption] = useState<string | number>();

    const updateOptions = () => {
        setOptions(Options.map((option: string | React.ReactElement): React.ReactElement => {
            if (typeof option === 'string')
                return <a key={ID} href='#' onClick={() => setSelectedOption(option)}> { option } </a>;
            
            return <a key={ID}> { option } </a>;
        }));
    };
    
    useEffect(() => updateOptions(), [Options]);
    useEffect(() => { 
        if (OnChange)
            OnChange(ID, selectedOption);
    }, [selectedOption]);

    return (
        <div className={classNames('dropdown', Disabled ? 'dropdown-disabled' : '')}>
            <button className='dropbtn' disabled> { Value } </button>
            <div className='dropdown-content'>
                { elementOptions }
                { StaticOptions && <div className={'additionalOptionsParent'}> { StaticOptions  } </div> }
            </div>
        </div>
    );
};

export default DropDownComponent;