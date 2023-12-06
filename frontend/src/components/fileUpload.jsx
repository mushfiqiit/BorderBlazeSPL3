import React, { useState } from 'react';
import MyForm from './methodChoice';

const FileUploadComponent = () => {
  const [file, setFile] = useState(null);
  const [imageSrc, setImageSrc] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setImageSrc(null); // Clear previous image when a new file is selected
  };

  const handleUpload = async () => {
    if (!file) {
      console.error('Please select a file before uploading.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/uploadfile/', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const contentType = response.headers.get('content-type');

        if (contentType && contentType.includes('image/png')) {
          // If the response is an image, convert it to a data URL
          const blob = await response.blob();
          const dataUrl = URL.createObjectURL(blob);
          console.log(dataUrl);
          setImageSrc(dataUrl);
        } else {
          console.error('Unexpected response content type:', contentType);
        }
      } else {
        console.error('Failed to upload file:', response.status, response.statusText);
      }
    } catch (error) {
      console.error('Error during file upload:', error);
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>

      {imageSrc && (
        <div>
          <p>Uploaded Image:</p>
          <img src={imageSrc} alt="Uploaded" style={{ maxWidth: '100%' }} />
        </div>
      )
      }

      {
        imageSrc && (
          <MyForm/>
        )
      }

    </div>
  );
};

export default FileUploadComponent;
