import { useState } from 'react';

interface McqProps {
    options: string[];
    correctAnswer: string;
    onSubmitAnswer: (selectedAnswer: string) => void;
}

function Mcq({ options, correctAnswer, onSubmitAnswer, }: McqProps) {
    const [selectedAnswer, setSelectedAnswer] = useState<string>('');

    const handleAnswerSelection = (answer: string) => {
        setSelectedAnswer(answer);
    };

    const handleSubmit = () => {
        if (selectedAnswer) {
            onSubmitAnswer(selectedAnswer);
        }
    };

    return (
        <div>
            {options.map((option, index) => (
                <div key={index} style={{ marginBottom: '10px' }}>
                    <button
                        onClick={() => handleAnswerSelection(String.fromCharCode(65 + index))}
                        style={{
                            padding: '10px',
                            width: '100%',
                            textAlign: 'left',
                            marginBottom: '5px',
                        }}
                    >
                        {String.fromCharCode(65 + index)}: {option}
                    </button>
                </div>
            ))}
            <button
                onClick={handleSubmit}
                disabled={!selectedAnswer}
                style={{
                    padding: '10px',
                    width: '100%',
                    backgroundColor: '#2196F3',
                    color: 'white',
                    border: 'none',
                    cursor: 'pointer',
                }}
            >
                Submit Answer
            </button>
        </div>
    );
}

export default Mcq;