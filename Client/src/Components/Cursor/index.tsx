import { useEffect, useRef } from 'react';

import './cursor-style.scss';
import { useSelector } from 'react-redux';
import { Cursor, StateTypes } from '../../Interfaces/StateInterface';

const CursorComponent = () => {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const canvaContainerRef = useRef<HTMLDivElement>(null);

    const cursor: Cursor = useSelector((state: StateTypes): Cursor => state.root.cursor);

    useEffect(() => {
        console.log(cursor);
        const canvas = canvasRef.current;
        const container = canvaContainerRef.current;
        if (canvas) {

            if (cursor === undefined)
                return;

            const ctx = canvas.getContext('2d');

            canvas.width = container.clientWidth;
            canvas.height = container.clientHeight;

            if (ctx) {
                // Calculate scale factors
                const scaleX = container.clientWidth / 1920;
                const scaleY = container.clientHeight / 1080;

                // Set the transformation matrix
                ctx.setTransform(scaleX, 0, 0, scaleY, 0, 0);

                // Clear the canvas
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                // Begin drawing the square
                ctx.beginPath();
                ctx.arc(cursor.x, cursor.y, 10, 0, 2 * Math.PI, false);
                ctx.closePath();

                // Optional: Set stroke and fill style
                ctx.strokeStyle = 'black';
                ctx.fillStyle = 'rgba(255, 255, 255, 0.20)';

                // Draw the square
                ctx.fill();
                ctx.stroke();    
            }
        }
    }, [cursor]);
    
    return (
        <div ref={canvaContainerRef} style={{ width:'100%', height:'100%', position: 'absolute' }}>
            <canvas
                ref={canvasRef}
                style={{ border: '1px solid black', display: 'block', width: '100%', height: '100%' }}
            />
        </div>
    );
};

export default CursorComponent;