import React, { useEffect, useRef, useState } from 'react';

import './heartbeat_style.scss';

interface HeartbeatProps {
  LastUpdated: number; // Epoch time in seconds (e.g., 1732890788.5043101)
  MaxPoints?: number,
}

const Heartbeat: React.FC<HeartbeatProps> = ({ LastUpdated, MaxPoints = 1500 }) => {
    const canvasRef = useRef<HTMLCanvasElement | null>(null);
    const animationRef = useRef<number | null>(null);
    const parentRef = useRef<HTMLDivElement>(null);

    const [Height, setHeight] = useState<number>(0);
    const [Width, setWidth] = useState<number>(0);

    // Data for the heartbeat waveform
    const points = useRef<number[]>(Array(MaxPoints).fill(0));
    let oldLastUpdated: number = null;

    useEffect(() => setHeight(parentRef.current?.clientHeight), [parentRef.current?.clientWidth]);
    useEffect(() => setWidth(parentRef.current?.clientWidth), [parentRef.current?.clientWidth]);

    // Function to calculate the next heartbeat value
    const calculateNextPoint = () => {
        const now = Date.now() / 1000; // Current time in seconds
        const timeDiff = now - LastUpdated;

        if (LastUpdated !== oldLastUpdated && timeDiff < 1) {
            oldLastUpdated = LastUpdated;
            // Peak when the update happened recently, decay otherwise
            return 1.25;
        }

        return Math.max(0, 1.25 - timeDiff / 1.15);
    };

    // Function to draw the heartbeat waveform on the canvas
    const draw = () => {
        const ctx = canvasRef.current?.getContext('2d');
        if (!ctx) return;

        // Calculate the next point and update the points array
        const nextPoint = calculateNextPoint();
        points.current.push(nextPoint);
        
        if (points.current.length > MaxPoints) {
            points.current.shift();
        }

        // Clear the canvas
        ctx.clearRect(0, 0, Width, Height);

        // Draw the heartbeat waveform
        ctx.beginPath();
        ctx.moveTo(0, Height / 2); // Start at the middle-left

        points.current.forEach((value, index) => {
            const x = (index / (MaxPoints - 1)) * Width; // Scale x to fit the canvas width
            const y = Height / 1.10 - value * (Height / 2); // Scale y based on value
            ctx.lineTo(x, y);
        });

        ctx.strokeStyle = 'red';
        ctx.lineWidth = 1;
        ctx.stroke();

        // Request the next animation frame
        animationRef.current = requestAnimationFrame(draw);
    };

    useEffect(() => {
        // Start the animation
        animationRef.current = requestAnimationFrame(draw);

        // Cleanup on component unmount
        return () => {
            if (animationRef.current) cancelAnimationFrame(animationRef.current);
        };
    }, [LastUpdated]);

    useEffect(() => {
        console.log(Height);
        console.log(Width);
    }, [Height, Width]);

    return <div className={'heartbeat-container'} ref={parentRef}>
        <canvas ref={canvasRef} width={Width} height={Height} />
    </div>
};

export default Heartbeat;
