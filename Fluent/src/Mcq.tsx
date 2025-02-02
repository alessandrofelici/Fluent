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
                <div key={index}>
                    <button
                        onClick={() => handleAnswerSelection(String.fromCharCode(65 + index))}
                        style={{ backgroundColor: selectedAnswer === String.fromCharCode(65 + index) ? '#4CAF50' : ''}}
                    >
                        {String.fromCharCode(65 + index)}: {option}
                    </button>
                </div>
            ))}
            <button onClick={handleSubmit} disabled={!selectedAnswer}>
                Submit Answer
            </button>
        </div>
    );
}

export default Mcq;