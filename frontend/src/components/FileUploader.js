import React, { useState } from 'react';
import { uploadFile } from './commonApi';
import '../styles/global.css';

const FileUploader = ({ setUploadedFiles }) => {
    const [dragging, setDragging] = useState(false);
    const [uploading, setUploading] = useState(false);
    const [uploadProgress, setUploadProgress] = useState(0);
    const [uploadedFiles, setUploadedFiles] = useState([]);

    const handleDragOver = (e) => {
        e.preventDefault();
        setDragging(true);
    };

    const handleDrop = async (e) => {
        e.preventDefault();
        setDragging(false);
        const file = e.dataTransfer.files[0];
        if (file) {
            setUploading(true);
            const progress = await uploadFile(file, setUploadProgress);
            setUploading(false);
            setUploadProgress(0);
            setUploadedFiles((prev) => [...prev, { name: file.name, type: file.type || 'unknown' }]);
        }
    };

    const handleFileClick = (file) => {
        
    }

    const handleDeleteFile = (fileName) => {
        // Add logic to delete file
    }

    const getFileIcon = (fileType) => {
        // Add logic to return icon based on file type
    }

    return (
        <div className={`chat-container ${dragging ? 'drag-over' : ''}`} onDragOver={handleDragOver} onDrop={handleDrop}>
            {/* Display uploaded files */}
            {uploadedFiles.map((file, index) => (
                <div key={index} className="uploaded-file">
                    <span className="file-icon">{getFileIcon(file.type)}</span>
                    <span className="file-name" onClick={() => handleFileClick(file)}>{file.name}</span>
                    <span className="delete-icon" onClick={() => handleDeleteFile(file.name)}>❌</span>
                </div>
            ))}
        </div>
    );
};

export default FileUploader;
