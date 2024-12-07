import Slider from '@mui/material/Slider';
import React, { useRef, useState, useEffect } from 'react';

const DateSlider = ({ minDate, maxDate, onDateChange }) => {
  const [value, setValue] = React.useState(maxDate);

  const handleChange = (event, newValue) => {
    setValue(newValue);
    onDateChange(newValue);
  };

  return (
    <div style={{ width: '300px', margin: '20px auto' }}>
      <Slider
        value={value}
        min={minDate}
        max={maxDate}
        step={1}
        onChange={handleChange}
        valueLabelDisplay="auto"
        valueLabelFormat={(value) => new Date(value).getFullYear()}
      />
    </div>
  );
};


export default DateSlider;