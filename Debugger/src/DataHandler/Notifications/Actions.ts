import { NotificationTypes, NotificationActionEnums } from '../../Common/enumerations';
import { getStore } from '../../Stores/store';

const sendNotification = (message: string, notificationType: number) => {
    const tempQueue = [{ message: message, type: notificationType }];
    getStore().dispatch({
        type: NotificationActionEnums.NewNotification,
        newQueue: tempQueue,
    });
};

export const notify = (message: string, notificationType = NotificationTypes.Info): any => sendNotification(message, notificationType);
export const notifySuccess = (message: string): any => sendNotification(message, NotificationTypes.Success);
export const notifyWarning = (message: string): any => sendNotification(message, NotificationTypes.Warning);
export const notifyError = (message: string): any => sendNotification(message, NotificationTypes.Error);