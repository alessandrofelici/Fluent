import Header from '../Header';
import { useState } from 'react';

function Flashcards() {
    const [card,setCard] = useState(['cat', 'gato'])
    const [vocab,setVocab] = useState(card[0])

    function handleFlip() {
        setTimeout(() => {
            vocab === card[0] ? setVocab(card[1]) : setVocab(card[0])
          }, 200);
        
    }

    function handleClick() {
        setCard(['dog','perro'])
        handleFlip()
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
                    <button className="nextcard" onClick={(handleClick)}>Next Card</button>
                </div>
            </body>
        </>
    )
}

export default Flashcards;