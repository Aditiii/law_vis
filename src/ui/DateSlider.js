import Slider from '@mui/material/Slider';
import React, { useEffect } from 'react';
import { Box } from '@mui/system';

const DateSlider = ({ minDate, maxDate, onDateChange, value }) => {
  const handleChange = (event, newValue) => {
    onDateChange(newValue);
  };

  useEffect(() => {
    // This effect will run when the component mounts or when value changes
    onDateChange(value);
  }, [value, onDateChange]);

  return (
    <div style={{ width: '80%', margin: '20px auto' }}>
          <Box
            sx={{
                flex: '3', // Adjust child2 width in parent
                display: 'flex',
                justifyContent: 'flex-end', // Align to the right
                alignItems: 'center', // Center vertically
                paddingRight: '20px', // Add spacing from the right edge
                backgroundColor: 'lightgreen', // Optional background for visualization
            }}
        >    <Slider
        value={value}
        min={minDate}
        max={maxDate}
        step={1}
        onChange={handleChange}
        valueLabelDisplay="auto"
        valueLabelFormat={(value) => new Date(value).toLocaleDateString()}
      />
      </Box>
    </div>
  );
};

export default DateSlider;