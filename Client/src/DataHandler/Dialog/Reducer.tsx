import { DialogActionEnums } from '../../Common/enumerations';
import { DialogStateInterface } from '../../Interfaces/StateInterface';

const initialResultState : DialogStateInterface = {
    dialog: null,
};

const reducer = (state = initialResultState, action: any = {}) => {
    const newState = { ...state };
    
    switch (action.type) {
        case DialogActionEnums.NewDialog:
            return {
                ...newState,
                dialog: action.newDialog,
            };
        case DialogActionEnums.ResetDialog:
            return {
                ...newState,
                dialog: null,
            };
        default:
            return { ...newState };
    }
};

export default reducer;