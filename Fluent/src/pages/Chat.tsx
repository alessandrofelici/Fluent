import { useState } from 'react'
import axios from 'axios'
import { Link } from 'react-router-dom'


interface Message {
  role: 'user' | 'assistant';
  content: string;
}

function Chat() {
  const [input, setInput] = useState<string>('');
  const [loading, setLoading] = useState(false)
  const [messages, setMessages] = useState<Message[]>([]);

  const handleSend = async () => {
    if (!input.trim()) return;
    setLoading(true)
    setMessages((prev) => [...prev, { role: 'user', content: input }]);
    setInput('');

    try {
      const response = await axios.post<{ reply: string }>('http://localhost:5000/chat', {message: input,});
      setLoading(false)
      const reply = response.data.reply;
      setMessages((prev) => [...prev, { role: 'assistant', content: reply}]);
    } catch (error) {
      setLoading(false)
      console.error('Error seding message:', error);
      setMessages((prev) => [...prev, { role: 'assistant', content: 'Failed to get response from AI.' },
      ]);
    }
  };

  return (
    <div>
      <h1>Fluent Chat</h1>
      <Link to="/">
        <button style={{ padding: '10px 20px', fontSize: '16px', marginBottom: '5px' }}>
          Go Back to Home
        </button>
      </Link>
      <div className="scroll-container">
        {messages.map((msg, index) => (<div className="bubble" key={index} style={{textAlign: msg.role === 'user' ? 'right' : 'left', marginBottom: '10px',}}> {msg.content} </div>))}
        {loading ? 'Loading...' : ''}
      </div>
      <input type="text" value={input} onChange={(e) => setInput(e.target.value)} onKeyPress={(e) => e.key === 'Enter' && handleSend()} style={{ width: '80%', padding: '10px' }} placeholder="Type a message..."/>
      <button onClick={handleSend} style={{ width: '40%', padding: '10px', marginLeft: '2%' }}>
        send
      </button>
    </div>
  );
}

export default Chat
