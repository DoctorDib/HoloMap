import { useEffect, useRef } from 'react';

import './spotlight-style.scss';
import { useSelector } from 'react-redux';
import { QR, StateTypes } from '../../../Interfaces/StateInterface';

const Spotlight = () => {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const canvaContainerRef = useRef<HTMLDivElement>(null);

    const qrs: QR = useSelector((state: StateTypes): QR => state.root.qr);

    useEffect(() => {
        const canvas = canvasRef.current;
        const container = canvaContainerRef.current;
        if (canvas) {

            if (qrs === undefined)
                return;

            const detected = qrs.detected_qrs;

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
                ctx.moveTo(detected[0][0][0], detected[0][0][1]);
                ctx.lineTo(detected[0][1][0], detected[0][1][1]);
                ctx.lineTo(detected[0][2][0], detected[0][2][1]);
                ctx.lineTo(detected[0][3][0], detected[0][3][1]);
                ctx.closePath();

                // Optional: Set stroke and fill style
                ctx.strokeStyle = 'black';
                ctx.fillStyle = 'lightblue';

                // Draw the square
                ctx.fill();
                ctx.stroke();
            }
        }
    }, [qrs]);
    
    return (
        <div ref={canvaContainerRef} style={{ width:'100%', height:'100%' }}>
            <canvas
                ref={canvasRef}
                style={{ border: '1px solid black', display: 'block' }}
            />
        </div>
    );
};

export default Spotlight;