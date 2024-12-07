import React, { useEffect, useState } from 'react';

import './modules_controller_style.scss';
import { ShowModuleInfo, UpdateCachedModules, WriteModuleSharedState } from '../../DataHandler/Root/Actions';
import { Module, Modules, StateTypes } from '../../Interfaces/StateInterface';
import { useSelector } from 'react-redux';
import ButtonComponent from '../Inputs/Button';
import Icons from '../../Common/Icons';

import buildTree from './buildTree'
import ModuleItemComponent from './moduleItem';
import { ModuleStateEnum } from '../../Common/enumerations';

const ModulesControllerComponent = (): React.ReactElement => {

    const modules: Modules = useSelector((state: StateTypes): Modules => state.root.modules);
    const viewedModule: string = useSelector((state: StateTypes): string => state.root.viewModule);

    const [tree, setTree] = useState<Module[]>(null);
    const [treeItems, setTreeItems] = useState<React.ReactElement[]>([]);
    const [childIndicator, setChildIndicator] = useState<any>({});
    const [selectedItem, setSelectedItem] = useState<Module>(null);

    const [disablePlay, setDisablePlay] = useState<boolean>(false);
    const [disableStop, setDisableStop] = useState<boolean>(false);
    const [disableReset, setDisableReset] = useState<boolean>(false);
    const [disablePause, setDisablePause] = useState<boolean>(false);
    
    useEffect(() => {
        if (modules === null || modules === undefined) {
            return;
        }

        // Updating the disabled states of the buttons
        checkControllerButtonStates();

        const [newTree, newModules] = buildTree(modules)
        setTree(newTree);
        
        UpdateCachedModules(newModules);
        
        const [treeItems, childIndicator] = generateTreeItems(newTree);
        setChildIndicator(childIndicator);
        setTreeItems(treeItems);
    }, [modules, selectedItem]);

    useEffect(() => {
        if (selectedItem?.Name !== viewedModule) {
            setSelectedItem(modules[viewedModule + '_module']);
        }
    }, [viewedModule])

    const checkControllerButtonStates = () => {

        if (selectedItem === undefined || selectedItem === null) {
            setDisableStop(true);
            setDisableReset(true);
            setDisablePlay(true);
            setDisablePause(true);
            return;
        }

        const currentSelectedItem = modules[selectedItem?.Name + '_module'];

        setDisableStop(false);
        setDisableReset(false);
        setDisablePlay(false);
        setDisablePause(false);

        // Custom conditions for states
        switch(currentSelectedItem?.State) {
            case ModuleStateEnum.RUNNING:
                setDisablePlay(true);
                break;
            case ModuleStateEnum.SET_PAUSE:
            case ModuleStateEnum.PAUSED:
                setDisablePause(true);
                break;
            case ModuleStateEnum.SET_STOP:
            case ModuleStateEnum.STOPPED:
                setDisablePlay(true);
                setDisableStop(true);
                setDisablePause(true);
                break;
            // Disable for transitional states
            case ModuleStateEnum.INITIALISING:
            case ModuleStateEnum.PAUSING:
            case ModuleStateEnum.STOPPING:
            case ModuleStateEnum.RELOADING:
            case ModuleStateEnum.RESUMING:
            // Disabling for errored states
            case ModuleStateEnum.NULL:
            case ModuleStateEnum.ERRORED:
            // Disabling for set events
            case ModuleStateEnum.SET_RELOAD:
            case ModuleStateEnum.SET_INIT:
            // Misc
            case ModuleStateEnum.RELOADED:
            case ModuleStateEnum.DISABLED:
                setDisableStop(true);
                setDisableReset(true);
                setDisablePlay(true);
                setDisablePause(true);
                break;
        }

        // Custom conditions for specific modules
        switch (currentSelectedItem?.Name) {
            case "Main":
                setDisableStop(true);
                setDisablePlay(true);
                setDisablePause(true);
                break;
            case "Health":
                setDisableStop(true);
                setDisablePlay(true);
                setDisablePause(true);
                break;
        }

        // Ensuring we can't click play if parent is paused
        const [isParentPaused, _] = checkIfParentIsPaused(currentSelectedItem?.Name, tree[0]?.Children);
        // Don't allow child to play if parent is paused
        if (isParentPaused) {
            setDisablePlay(true);
        }

        // Ensuring a stopped parent item is unable to reload as it just wont work
        currentSelectedItem?.State === ModuleStateEnum.STOPPED ? setDisableReset(true) : setDisableReset(false);

        // PERMANENTLY DISABLE
        // Special conditions based on module items
        if (!childIndicator[currentSelectedItem?.Name]) { // && currentSelectedItem?.Name !== "Health") {
            setDisableReset(true);
        }
    };

    const checkIfParentIsPaused = (keyToSearch: string, children: Module[]): [boolean, boolean] => {
        const shouldDisableStates: any = [
            ModuleStateEnum.PAUSED,
            ModuleStateEnum.PAUSING,
            ModuleStateEnum.STOPPING,
            ModuleStateEnum.RELOADING,
            ModuleStateEnum.RESUMING,
        ];

        for (let i = 0; i < children.length; i++) {
            const child = children[i];

            if (child.Name === keyToSearch) {
                return [null, true];
            }

            if (child?.Children.length > 0) {
                const [isParentPaused, found] = checkIfParentIsPaused(keyToSearch, child.Children);

                if (found && isParentPaused === null) {
                    const stateMatches = shouldDisableStates.includes(child.State);
                    return [stateMatches, true];
                }
                else if (found) {
                    return [isParentPaused, true];
                }
            }
        }

        // No item found
        return [false, false];
    };

    const generateTreeItems = (treeModules: Module[]): [React.ReactElement[], object] => {
        const items = [];

        let childIndicatorTemp: any = {};

        for (let i = 0; i < treeModules.length; i++) {
            const treeItem = treeModules[i];

            if (treeItem.Children.length > 0) {
                const [childItems, childIndicatorTempTemp] = generateTreeItems(treeItem.Children);
                childIndicatorTemp = {
                    ...childIndicatorTemp,
                    ...childIndicatorTempTemp,
                }
                
                childIndicatorTemp[treeItem.Name] = true;

                items.push(<ModuleItemComponent key={treeItem.Name} Module={treeItem} Children={childItems} 
                                                SetSelectedItem={(key: Module) => setSelectedItem(key)} 
                                                SelectedItem={selectedItem} />);

                continue;
            } 

            childIndicatorTemp[treeItem.Name] = false;
                
            items.push(<ModuleItemComponent key={treeItem.Name} Module={treeItem} 
                SetSelectedItem={(key: Module) => setSelectedItem(key)} 
                SelectedItem={selectedItem} />);    
        };

        return [items, childIndicatorTemp];
    };

    return <>
        <div className={'module-control'}>
            <div className={'module-title'}>Module Control</div>

            <div className={'module-controller'}>
                <div className={'controller-name'}> 
                    <div>
                        { selectedItem === undefined || selectedItem === null ? 'N/A' : selectedItem?.Name } 
                    </div>
                    <div>
                        { selectedItem === undefined || selectedItem === null ? 'N/A' : modules[selectedItem?.Name + '_module']?.State } 
                    </div>
                    
                </div>

                <div className={'controller-buttons-container'}>
                    <ButtonComponent Icon={Icons.Play} Disabled={disablePlay}
                                    OnClick={() => WriteModuleSharedState(selectedItem?.Name, "play")} />
                    <ButtonComponent Icon={Icons.Pause} Disabled={disablePause} 
                                    OnClick={() => WriteModuleSharedState(selectedItem?.Name, "pause")} />
                    <ButtonComponent Icon={Icons.Stop} Disabled={disableStop} 
                                    OnClick={() => WriteModuleSharedState(selectedItem?.Name, "stop")} />
                    <ButtonComponent Icon={Icons.Reset} Disabled={disableReset} 
                                    OnClick={() => WriteModuleSharedState(selectedItem?.Name, "reload")} />
                    <ButtonComponent Icon={Icons.Info}
                                    OnClick={() => ShowModuleInfo(selectedItem?.Name)} />
                </div>
            </div>

            <div className={'module-list'}>
                {treeItems}
            </div>
        </div>
    </>;
};

export default ModulesControllerComponent;