import React, { ReactNode, useEffect, useState } from 'react';

import './aspect_container_style.scss';
import { useSelector } from 'react-redux';
import { StateTypes } from '../../Interfaces/StateInterface';

interface AspectContainerInterface {
    Width?: string,
    Height?: string,
    children?: ReactNode
}

const AspectContainerComponent = ({ children, Width = "100%", Height = "100%", }: AspectContainerInterface): React.ReactElement => {
    const readonlyBoundary: any = useSelector((state: StateTypes): any => state.calibrations.projector.readonly_boundary);

    const [xScale, setXScale] = useState<number>(0);
    const [yScale, setYScale] = useState<number>(0);

    const getAspectRatioPercentageDifference = (width: number, height: number): { widthPercentage: number, heightPercentage: number } => {
        const targetAspectRatio = 16 / 9;
        const currentAspectRatio = width / height;
    
        let widthPercentage = 0;
        let heightPercentage = 0;
    
        if (currentAspectRatio > targetAspectRatio) {
            // Width is too large for 16:9, calculate the percentage difference in width
            const idealWidth = height * targetAspectRatio;
            widthPercentage = ((width - idealWidth) / width) * 100; // Calculate the percentage difference
        } else if (currentAspectRatio < targetAspectRatio) {
            // Height is too large for 16:9, calculate the percentage difference in height
            const idealHeight = width / targetAspectRatio;
            heightPercentage = ((height - idealHeight) / height) * 100; // Calculate the percentage difference
        }
    
        return { widthPercentage, heightPercentage };
    }

    useEffect(() => {
        if (Object.keys(readonlyBoundary).length !== 0 && readonlyBoundary !== undefined) {
            const coord = readonlyBoundary['main-content'].corners;
            const width = coord[2] - coord[0];
            const height = coord[5] - coord[3];

            const aspectRatioDifferences = getAspectRatioPercentageDifference(width, height);

            setXScale(1-aspectRatioDifferences.widthPercentage / 100);
            setYScale(1-aspectRatioDifferences.heightPercentage / 100);
        }        
    }, [readonlyBoundary]);

    return (
        <div style={{ 
                width: Width, 
                height: Height,
                transform: `scale(${xScale}, ${yScale})`,
            }}>
                {children}
        </div>
    );
};

export default AspectContainerComponent;