import React from 'react';
import { deleteFile } from './commonApi';
import '../styles/global.css';

const FileList = ({ uploadedFiles, setUploadedFiles }) => {
    const handleDeleteFile = async (fileName) => {
        await deleteFile(fileName);
        setUploadedFiles((prev) => prev.filter((file) => file.name !== fileName));
    };

    return (
        <div className="uploaded-files">
            {uploadedFiles.map((file, index) => (
                <div key={index} className="uploaded-file">
                    <span className="file-name">{file.name}</span>
                    <span className="delete-icon" onClick={() => handleDeleteFile(file.name)}>❌</span>
                </div>
            ))}
        </div>
    );
};

export default FileList;
