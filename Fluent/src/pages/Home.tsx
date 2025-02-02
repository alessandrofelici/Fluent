import React from 'react';
import { Link } from 'react-router-dom';
import Header from '../Header';

function Home() {
    return (
        <div>
            <><div style={{
                position: 'fixed',
                top: 0,
                left: 0,
                right: 0,
                backgroundColor: '#000',
                padding: '10px',
                boxShadow: '0 2px 4px rgba(112, 112, 112, 0.1)',
                zIndex: 1000,
            }}>
            <h1>
                Fluent !
            </h1>
            </div></>
            <h1>How would you like to study?</h1>
            <Link to="/Chat">
                <button className="pages" style={{ padding: '10px 20px',
                                 fontSize: '16px'}}>
                Conversation
                </button>
            </Link>
            <Link to="/Quiz">
                <button className="pages" style={{ padding: '10px 20px',
                                 fontSize: '16px'}}>
                Quiz
                </button>
            </Link>
            <Link to="/Flashcards">
                <button className="pages" style={{ padding: '10px 20px',
                                 fontSize: '16px'}}>
                Flashcards
                </button>
            </Link>
        </div>
    );
}

export default Home;