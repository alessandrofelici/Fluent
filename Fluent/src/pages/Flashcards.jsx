import Header from '../Header';
import { useState } from 'react';

function Flashcards() {
    const [vocab,setVocab] = useState('dog')

    function handleFlip() {
        vocab === 'dog' ? setVocab('perro') : setVocab('dog')
    }

    return (
        <>
            <div>
                <Header />
            </div>
            <body>
                <div className="flip-button">
                    <div className="flip-content">
                        <div className="flip-front" onMouseEnter={(handleFlip)}>{vocab}</div>
                        <div className="flip-back" onMouseLeave={(handleFlip)}>{vocab}</div>
                    </div>
                    <button>Next Card</button>
                </div>
            </body>
        </>
    )
}

export default Flashcards;