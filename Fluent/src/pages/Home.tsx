import React from 'react';
import { Link } from 'react-router-dom';
import Header from '../Header';

function Home() {
    return (
        <div>
            <Header/>
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