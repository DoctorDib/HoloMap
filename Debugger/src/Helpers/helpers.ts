const copyTextToClipboard = async (text: string): Promise<boolean | void> => {
    if ('clipboard' in navigator) {
        return navigator.clipboard.writeText(text);
    }
    return document.execCommand('copy', true, text);
};

export { copyTextToClipboard };