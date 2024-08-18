import { DialogActionEnums } from '../../Common/enumerations';
import { DialogOptionsInterface } from '../../Interfaces/StateInterface';
import { getStore } from '../../Stores/store';

export const dialog = (header: string, message: string, options: Array<DialogOptionsInterface>): any => 
    getStore().dispatch({
        type: DialogActionEnums.NewDialog,
        newDialog: { header: header, message: message, options: options },
    });

export const resetDialog = () => getStore().dispatch({ type: DialogActionEnums.ResetDialog });