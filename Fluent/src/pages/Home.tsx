import React from 'react';
import { Link } from 'react-router-dom';
import Header from '../Header';

function Home() {
    return (
        <div>
            <Header/>
            <h1>Welcome to Fluent! Click below to start a conversation!</h1>
            <Link to="/chat">
                <button className="pages" style={{ padding: '10px 20px',
                                 fontSize: '16px'}}>
                Go to Chat
                </button>
            </Link>
            <Link to="/Quiz">
                <button className="pages" style={{ padding: '10px 20px',
                                 fontSize: '16px'}}>
                Go to Quiz
                </button>
            </Link>
        </div>
    );
}

export default Home;