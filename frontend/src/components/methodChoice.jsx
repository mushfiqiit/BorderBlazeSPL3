import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

const MyForm = () => {
  const [selectedOption, setSelectedOption] = useState(1);
  const [imageSrc, setImageSrc] = useState(null);

  const handleOptionChange = (option) => {
    setSelectedOption(option);
  };

  const handleFormSubmit = (event) => {
    event.preventDefault();

    // Make a GET request with the selected option
    fetch(`http://127.0.0.1:800${selectedOption}/method/${selectedOption}`)
      .then(response => response.blob())
      .then(blob => {
        // Convert the blob to a data URL
        const imageUrl = URL.createObjectURL(blob);
        
        // Set the image source
        setImageSrc(imageUrl);
      })
      .catch(error => {
        // Handle errors
        console.error('Error:', error);
      });
  };

  return (
    <div className="container mt-4">
      <form onSubmit={handleFormSubmit}>
        <div className="mb-3">
          <label className="form-label">Choose an option:</label>
          <select
            className="form-select"
            value={selectedOption}
            onChange={(e) => handleOptionChange(e.target.value)}
          >
            <option value={1}>Method 1: Neighborhood Based Approach</option>
            <option value={2}>Method 2: Concave Hull Algorithm</option>
            <option value={3}>Method 3: Delaunay Triangulation</option>
          </select>
        </div>
        <button type="submit" className="btn btn-primary">Submit</button>
      </form>

      {imageSrc && (
        <div className="mt-4">
          <p>Received Image:</p>
          <img src={imageSrc} alt="Output Image" className="img-fluid" />
        </div>
      )}
    </div>
  );
};

export default MyForm;
