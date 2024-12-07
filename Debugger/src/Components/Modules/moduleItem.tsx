import React, { useState } from 'react';

import './modules_controller_style.scss';
import { Module } from '../../Interfaces/StateInterface';
import ButtonComponent from '../Inputs/Button';
import Icons from '../../Common/Icons';

import classNames from 'classnames';
import { ModuleStateEnum } from '../../Common/enumerations';

interface ModuleItemInterface {
    Module: Module;
    Children?: React.ReactElement[];
    SelectedItem: Module;
    SetSelectedItem: (key: Module) => void;
}

const ModuleItemComponent = ({ Module, Children, SetSelectedItem, SelectedItem }: ModuleItemInterface) : React.ReactElement => {
    const [hideChildren, setHideChildren] = useState<boolean>(false);
    
    const ShouldBlink = (status: string) => {
        const blinkingStates: any = [
            ModuleStateEnum.PAUSING,
            ModuleStateEnum.STOPPING,
            ModuleStateEnum.RELOADING,
            ModuleStateEnum.RESUMING,
            ModuleStateEnum.ERRORED,
        ];

        return blinkingStates.includes(status) ? '1' : '0';
    };

    return <div key={Module.Name} className={'module-item-component'}> 
        <div className={'item-container'}>
            <div className={classNames([SelectedItem?.Name === Module.Name ? 'selected-item' : '', 'item'])}
                onClick={() => SetSelectedItem(Module)}>
                    
                <div className={'item-left'}> 
                    {
                        Children !== null && Children !== undefined ? (
                            <ButtonComponent Icon={hideChildren ? Icons.ArrowRight : Icons.ArrowDown} OnClick={() => setHideChildren(!hideChildren)} />
                        ) : null
                    }

                    <div className={'item-name'}> { Module.Name } </div>
                </div>

                <div className={classNames(['status-colour', Module.State])}>
                    <div style={{ 
                        animation: `blinker ${ShouldBlink(Module.State)}s infinite linear`,
                        width: '100%',
                        height: '100%',
                    }}/>

                    <div className={'tooltip'}>
                        <span className={'tooltiptext'}> { Module.State } </span>
                    </div>
                </div>
            </div>

            {
                Children !== null && Children !== undefined ? (
                    <div className={'children-items'} style={{ display: hideChildren ? 'none' : 'flex' }}> { Children } </div>
                ) : null
            }
        </div>
    </div>
};

export default ModuleItemComponent;