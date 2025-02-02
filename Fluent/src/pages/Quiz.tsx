import { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom'
import Mcq from '../Mcq';
import Header from '../Header';

function Quiz() {
    const [language, setLanguage] = useState<string>('');
    const [question, setQuestion] = useState<string>('');
    const [options, setOptions] = useState<string[]>([]);
    const [correctAnswer, setCorrectAnswer] = useState<string>('');
    const [result, setResult] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);

    const handleGetQuestion = async () => {
        if (!language.trim()) return;
        setLoading(true);
    
        try {
            const response = await axios.post<{ question: string, options: string[], correctAnswer: string }>('http://localhost:5000/quiz', { language });
    
            console.log("API Response:", response.data); // Debugging: Log the API response
    
            // Ensure the options array has exactly 4 elements
            const validatedOptions = response.data.options.length === 4 
                ? response.data.options 
                : ["Option A", "Option B", "Option C", "Option D"];
    
            setQuestion(response.data.question);
            setOptions(validatedOptions);
            setCorrectAnswer(response.data.correctAnswer)
        } catch (error) {
            console.error('Error fetching question:', error);
            setResult('Failed to fetch a question. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleSubmitAnswer = async (selectedAnswer: string) => {
        if (!selectedAnswer.trim()) return;
        setLoading(true);

        try {
            const response = await axios.post<{ result: string }>('http://localhost:5000/quiz/check', { userAnswer: selectedAnswer });
            setResult(response.data.result);
        } catch (error) {
            console.error('Error checking answer:', error);
            setResult('Failed to check the answer. Please try again.');
        } finally {
            setLoading(false); // Ensure loading is set to false after the request
        }
    };

    return (
        <>
            <div style={{ paddingTop: '100px' }}>
                <Header/>
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
                            <Mcq options={options} correctAnswer={correctAnswer} onSubmitAnswer={handleSubmitAnswer} />
                        </div>
                )}
                {result && (
                    <div>
                        <h3>Result:</h3>
                        <p>{result}</p>
                    </div>
                )}
            </div>
        </>
    );
}

export default Quiz;