import { useState, useEffect } from 'react';

export enum MouseButton {
    None = 0,
    LeftMouse = 1,
    MiddleMouse = 2,
    RightMouse = 3,
}

interface MousePosition { x: number, y: number }

interface MouseProperties {
    state: MouseButton,
    position: MousePosition,
}

const useMouseProperties = (): MouseProperties => {
    const [mouseState, setMouseState] = useState<MouseButton>(MouseButton.None);
    const [mousePosition, setMousePosition] = useState<MousePosition>({ x: 0, y: 0 });

    useEffect(() => {
        const handleMouseDown = (event: MouseEvent) => {
            switch (event.button) {
                case 0:
                    setMouseState(MouseButton.LeftMouse);
                    break;
                case 1:
                    setMouseState(MouseButton.MiddleMouse);
                    break;
                case 2:
                    setMouseState(MouseButton.RightMouse);
                    break;
                default:
                    setMouseState(MouseButton.None);
                    break;
            }
        };

        const handleMouseUp = () => {
            setMouseState(MouseButton.None);
        };

        const handleMouseMove = (event: MouseEvent) => setMousePosition({ x: event.clientX, y: event.clientY });

        document.addEventListener('mousedown', handleMouseDown);
        document.addEventListener('mouseup', handleMouseUp);
        document.addEventListener('mousemove', handleMouseMove);

        return () => {
            document.removeEventListener('mousedown', handleMouseDown);
            document.removeEventListener('mouseup', handleMouseUp);
            document.removeEventListener('mousemove', handleMouseMove);
        };
    }, []);

    return { state: mouseState, position: mousePosition };
};

export default useMouseProperties;