import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
    return (
        <div>
            <h1>Fluent</h1>
            <p>Welcome to Fluent! Click below to start a conversation!</p>
            <Link to="/chat">
                <button style={{ padding: '10px 20px',
                                 fontSize: '16px'}}>
                Go to Chat
                </button>
            </Link>
        </div>
    );
}

export default Home;