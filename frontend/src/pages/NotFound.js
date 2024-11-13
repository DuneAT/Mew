import React from 'react';
import { Link } from 'react-router-dom';

const NotFound = () => {
    return (
        <div style={styles.container}>
            <h1 style={styles.header}>404 - Page Not Found</h1>
            <p style={styles.message}>Sorry, the page you are looking for does not exist.</p>
            <Link to="/" style={styles.link}>Go back to Home</Link>
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
        textAlign: 'center',
    },
    header: {
        fontSize: '3rem',
        color: '#ff6b6b',
    },
    message: {
        fontSize: '1.2rem',
        color: '#555',
        marginBottom: '20px',
    },
    link: {
        fontSize: '1rem',
        color: '#3498db',
        textDecoration: 'none',
    },
};

export default NotFound;
