import { NotificationActionEnums } from '../../Common/enumerations';
import { NotificationQueueInterface } from '../../Interfaces/StateInterface';

const initialResultState : NotificationQueueInterface = {
    queue: [],
};

const reducer = (state = initialResultState, action: any = {}) => {
    const newState = { ...state };
    
    switch (action.type) {
        case NotificationActionEnums.NewNotification:
            if (action.newQueue === undefined) {
                return newState;
            } 
            return {
                ...newState,
                queue: [...state.queue, ...action.newQueue],
            };
        default:
            return { ...newState };
    }
};

export default reducer;