import React, { useEffect } from 'react';
import { useSelector } from 'react-redux';

import { ToastContainer, toast, ToastOptions } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { NotificationTypes } from '../../Common/enumerations';
import { NotificationInterface, NotificationQueueInterface, StateTypes } from '../../Interfaces/StateInterface';

const NotificationComponent = (): React.ReactElement => {

    const notifications = useSelector((state: StateTypes): NotificationQueueInterface => state.notification);

    const toastOptions: ToastOptions = {
        position: 'bottom-center',
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: 0,
    };

    const handleNotification = () => {
        if (notifications.queue.length <= 0) {
            return;
        }

        notifications.queue.forEach((notification: NotificationInterface): void => {
            if (notification.message === '') {
                return;
            }

            switch (notification.type) {
                case NotificationTypes.Info:
                    toast.info(notification.message, toastOptions);
                    break;
                case NotificationTypes.Success:
                    toast.success(notification.message, toastOptions);
                    break;
                case NotificationTypes.Warning:
                    toast.warning(notification.message, toastOptions);
                    break;
                case NotificationTypes.Error:
                    toast.error(notification.message, toastOptions);
                    break;
                default:
                    toast(notification.message, toastOptions);
            }
        });

        notifications.queue = [];
    };

    useEffect(() => { handleNotification(); }, [notifications.queue]);
    
    return (
        <ToastContainer
            position="bottom-center"
            autoClose={2500}
            hideProgressBar={false}
            newestOnTop={false}
            closeOnClick
            rtl={false}
            pauseOnFocusLoss
            draggable
            pauseOnHover
        />
    );
};

export default NotificationComponent;