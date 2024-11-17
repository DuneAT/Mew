import React from 'react';
import { useNavigate } from 'react-router-dom';

const HomePage = () => {
    const navigate = useNavigate();

    const handleNavigate = (path) => {
        navigate(path);
    };

    return (
        <div style={styles.container}>
            <h1 style={styles.header}>Choose a Tool</h1>
            <div style={styles.buttonContainer}>
                <button style={styles.button} onClick={() => handleNavigate('/conversation')}>Conversation</button>
                <button style={styles.button} onClick={() => handleNavigate('/rag')}>RAG (Retrieval-Augmented Generation)</button>
                <button style={styles.button} onClick={() => handleNavigate('/legifrance')}>RAG Legifrance</button>
                <button style={styles.button} onClick={() => handleNavigate('/other-tool')}>Other Tool</button>
            </div>
        </div>
    );
};

const styles = {
    container: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
        backgroundColor: '#f5f5f5',
    },
    header: {
        fontSize: '2rem',
        marginBottom: '20px',
    },
    buttonContainer: {
        display: 'flex',
        gap: '20px',
    },
    button: {
        padding: '10px 20px',
        fontSize: '1.2rem',
        cursor: 'pointer',
        borderRadius: '5px',
        border: 'none',
        backgroundColor: '#4CAF50',
        color: 'white',
        transition: 'background-color 0.3s ease',
    }
};

export default HomePage;
