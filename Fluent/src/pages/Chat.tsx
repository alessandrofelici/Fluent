import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import Header from '../Header';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

function Chat() {
  const [input, setInput] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [languageSet, setLanguageSet] = useState(false); // Track if language is set
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Initial message from the AI asking for the language
    if (!languageSet) {
      setMessages([{ role: 'assistant', content: 'Hi! What language would you like to practice?' }]);
    }
  }, [languageSet]);

  useEffect(() => {
    // Scroll to the bottom whenever messages change
    if (scrollContainerRef.current) {
      scrollContainerRef.current.scrollTop = scrollContainerRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setMessages((prev) => [...prev, { role: 'user', content: input }]);
    setInput('');

    try {
      const response = await axios.post<{ reply: string }>('http://localhost:5000/chat', { message: input });
      setLoading(false);
      const reply = response.data.reply;

      // If the language is not set, assume the first user input is the language
      if (!languageSet) {
        setLanguageSet(true);
      }

      setMessages((prev) => [...prev, { role: 'assistant', content: reply }]);
    } catch (error) {
      setLoading(false);
      console.error('Error sending message:', error);
      setMessages((prev) => [...prev, { role: 'assistant', content: 'Failed to get response from AI.' }]);
    }
  };

  return (
    <div>
      <Header />
      <div className="scroll-container" ref={scrollContainerRef} style={{ height: '400px', overflowY: 'auto', border: '1px solid #ccc', padding: '10px', marginBottom: '10px' }}>
        {messages.map((msg, index) => (
          <div className="bubble" key={index} style={{ textAlign: msg.role === 'user' ? 'right' : 'left', marginBottom: '10px' }}>
            {msg.content}
          </div>
        ))}
        {loading ? 'Loading...' : ''}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
        style={{ width: '80%', padding: '10px' }}
        placeholder="Type a message..."
      />
      <button onClick={handleSend} style={{ width: '40%', padding: '10px', marginLeft: '2%' }}>
        Send
      </button>
    </div>
  );
}

export default Chat;