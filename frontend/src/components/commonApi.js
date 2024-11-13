export const uploadFile = async (file, setUploadProgress) => {
    const formData = new FormData();
    formData.append('file', file);
    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://localhost:8000/api/upload');
    xhr.upload.onprogress = (event) => {
        if (event.lengthComputable) {
            setUploadProgress((event.loaded / event.total) * 100);
        }
    };
    xhr.send(formData);
};

export const deleteFile = async (fileName) => {
    await fetch(`http://localhost:8000/api/delete-file?file_name=${encodeURIComponent(fileName)}`, { method: 'DELETE' });
};
