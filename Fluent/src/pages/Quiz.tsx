import { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom'

function Quiz() {
    const [language, setLanguage] = useState<string>('');
    const [question, setQuestion] = useState<string>('');
    const [userAnswer, setUserAnswer] = useState<string>('');
    const [result, setResult] = useState<string>('');
    const [loading, setloading] = useState<boolean>(false);

    const handleGetQuestion = async () => {
        if (!language.trim()) return;
        setloading(true);

        try{
            const response = await axios.post<{ question: string }>('http://localhost:5000/quiz', { language, });
            setQuestion(response.data.question);
            setResult('');
            setUserAnswer('');
        } catch (error) {
            console.error('Error fetching question:', error);
            setResult('Failed to fetch a question. Please try again.');
            setloading(false);
        }
    };

    const handleSubmitAnswer = async () => {
        if (!userAnswer.trim()) return;
        setloading(true);

        try{
            const response = await axios.post<{ result: string }>('http://localhost:5000/quiz/check', { language, question, userAnswer,});
            setResult(response.data.result);
        } catch (error) {
            console.error('Error checking answer:', error);
            setResult('Failed to check the answer. Please try again.');
            setloading(false);
        }
    };

    return (
        <div style={{ paddingTop: '100px' }}>
            <div style={{
                position: 'fixed',
                top: 0,
                left: 0,
                right: 0,
                backgroundColor: '#000',
                padding: '10px',
                boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
                zIndex: 1000,
            }}>
                <h1><Link to="/">
                    <button style={{ 
                        padding: '10px 20px',
                        fontSize: '16 px',
                        marginBottom: '5px',
                        position: 'absolute',
                        left: '10px',
                    }}>
                    Home
                    </button>
                    </Link>
                    Fluent Quiz
                </h1>
            </div>
            <div>
                <input 
                type="text" 
                value={language} 
                onChange={(e) => setLanguage(e.target.value)} 
                placeholder="Enter language" 
                style={{ width: '80%', padding: '10px', marginBottom: '10px'}}
                />
                <button 
                    onClick={handleGetQuestion} 
                    style={{ width: '40%', padding: '10px', marginLeft: '2%' }} 
                    disabled={loading}
                    >
                    {loading ? 'Loading...' : 'Get Question'}
                </button>
            </div>
            {question && (
                <div>
                    <h3>Question</h3>
                    <p>{question}</p>
                    <input 
                        type="text" 
                        value={userAnswer} 
                        onChange={(e) => setUserAnswer(e.target.value)} 
                        placeholder="Your answer" 
                        style={{ width: '80%', padding: '10px', marginBottom: '10px' }}
                        />
                    <button 
                        onClick={handleSubmitAnswer} 
                        style={{ width: '40%', padding: '10px', marginLeft: '2%' }} 
                        disabled={loading}
                        >
                            {loading ? 'Loading...': 'Submit Answer'}
                    </button>
                </div>
            )}
            {result && (
                <div>
                    <h3>Result:</h3>
                    <p>{result}</p>
                </div>
            )}
        </div>
    );
}

export default Quiz;