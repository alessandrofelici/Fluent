import { BrowserRouter as Router,  Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Chat from './pages/Chat';
import Quiz from './pages/Quiz';
import './App.css';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/Chat" element={<Chat />} />
                <Route path="/Quiz" element={<Quiz />} />
            </Routes>
        </Router>
    );
}

export default App;