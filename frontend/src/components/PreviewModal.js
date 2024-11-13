import React from 'react';
import '../styles/global.css';

const PreviewModal = ({ selectedFile, closePreview }) => (
    <div className="preview-modal">
        <div className="preview-content">
            <button onClick={closePreview} className="close-button">Close</button>
            {/* Add preview display logic based on file type */}
        </div>
    </div>
);

export default PreviewModal;
