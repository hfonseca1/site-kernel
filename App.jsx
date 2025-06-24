import React, { useState } from 'react';
import axios from 'axios';

export default function MultiReturnImageUpload() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [images, setImages] = useState({});

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = () => {
    if (!selectedFile) {
      alert('Selecione uma imagem primeiro.');
      return;
    }

    const formData = new FormData();
    formData.append('image', selectedFile);

    axios.post('http://localhost:5000/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
      .then(response => {
        setImages(response.data);  // O backend retorna as imagens em base64
      })
      .catch(error => {
        console.error('Erro ao enviar imagem:', error);
      });
  };

  return (
    <div>
      <h2>Upload de Imagem (usando Axios)</h2>

      <input type="file" accept="image/*" onChange={handleFileChange} />
      <button onClick={handleUpload}>Enviar Imagem</button>

      <div style={{ display: 'flex', flexWrap: 'wrap', marginTop: '20px' }}>
        {Object.entries(images).map(([tipo, base64], index) => (
          <div key={index} style={{ margin: '10px' }}>
            <h4>{tipo}</h4>
            <img
              src={`data:image/jpeg;base64,${base64}`}
              alt={tipo}
              style={{ maxWidth: '300px' }}
            />
          </div>
        ))}
      </div>
    </div>
  );
}
