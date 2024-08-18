import  axios, { AxiosError, AxiosRequestConfig } from 'axios';

export const sendData = async (url: string, bodyData: object = {}): Promise<string> => {
    url = `${window.location.protocol}//${window.location.hostname}:5000${url}`;

    const options: AxiosRequestConfig = {
        method: 'POST',
        data: { ...bodyData },
        url: url,
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json;',
            'Access-Control-Allow-Origin': '*',
        },
    };

    return axios(options)
        .then((response: any) => response.data) //inspectObjectArray(true, response.data))
        .catch((error: AxiosError) => {
            console.log('Axios Error search Peanut:', error);
        });
};