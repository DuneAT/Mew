import React, { useState } from 'react';
import FileUploader from '../../components/FileUploader';
import FileList from '../../components/FileList';
import PreviewModal from '../../components/PreviewModal';
import { fetchUploadedFiles, deleteFile } from '../../components/commonApi';
import '../../styles/global.css';

const RAG = () => {
    const [uploadedFiles, setUploadedFiles] = useState([]);
    const [selectedFile, setSelectedFile] = useState(null);

    return (
        <div className="rag-container">
            <FileUploader setUploadedFiles={setUploadedFiles} />
            <FileList
                uploadedFiles={uploadedFiles}
                setUploadedFiles={setUploadedFiles}
                onFileClick={setSelectedFile}
            />
            {selectedFile && (
                <PreviewModal selectedFile={selectedFile} closePreview={() => setSelectedFile(null)} />
            )}
        </div>
    );
};

export default RAG;
