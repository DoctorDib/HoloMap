import { useState } from 'react';

import './slider_style.scss';

interface SliderComponentInterface {
    Text?: string | boolean | number | React.ReactElement,
    Icon?: React.ReactElement,
    Disabled?: boolean,
    ClassName?: any,
    CustomStyle?: any,

    Min: number;
    Max: number;
    Step?: number;
    Value: number;
    OnChange: (value: number) => void;
}

const SliderComponent = ({ Text, Icon, Disabled, ClassName, CustomStyle, Min, Max, Step, Value, OnChange
 }: SliderComponentInterface) => {
    const [currentValue, setCurrentValue] = useState(Value);

    const handleSliderChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const newValue = Number(event.target.value);
        setCurrentValue(newValue);
        OnChange(newValue);
    };
  
    return (
      <div className="slider-container">
        {Text && <label>{Text}</label>}
        <input
            type="range"
            min={Min}
            max={Max}
            step={Step}
            value={currentValue}
            onChange={handleSliderChange}
            className="slider"
        />
        <span className="slider-value">{currentValue}</span>
      </div>
    );
};

export default SliderComponent;