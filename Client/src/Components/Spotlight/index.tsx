import { useEffect, useRef } from 'react';

import './spotlight-style.scss';
import { useSelector } from 'react-redux';
import { ArUco, StateTypes } from '../../Interfaces/StateInterface';

const Spotlight = () => {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const canvaContainerRef = useRef<HTMLDivElement>(null);

    const arucos: ArUco = useSelector((state: StateTypes): ArUco => state.root.aruco);

    useEffect(() => {
        const canvas = canvasRef.current;
        const container = canvaContainerRef.current;
        if (canvas) {

            if (arucos === undefined || arucos.detected_arucos === undefined)
                return;

            const detected = arucos.detected_arucos;

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

                if (detected.length > 0) {
                    // Begin drawing the square
                    ctx.beginPath();
                    ctx.moveTo(detected[0][0][0], detected[0][0][1]);
                    ctx.lineTo(detected[0][1][0], detected[0][1][1]);
                    ctx.lineTo(detected[0][2][0], detected[0][2][1]);
                    ctx.lineTo(detected[0][3][0], detected[0][3][1]);
                    ctx.closePath();

                    // Optional: Set stroke and fill style
                    ctx.strokeStyle = 'black';
                    ctx.fillStyle = 'rgba(255, 255, 255, 0.20)';

                    // Draw the square
                    ctx.fill();
                    ctx.stroke();    
                }
            }
        }
    }, [arucos]);
    
    return (
        <div ref={canvaContainerRef} style={{ width:'100%', height:'100%', position: 'absolute' }}>
            <canvas
                ref={canvasRef}
                style={{ border: '1px solid black', display: 'block', width: '100%', height: '100%' }}
            />
        </div>
    );
};

export default Spotlight;