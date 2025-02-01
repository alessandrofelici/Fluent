import { useState } from 'react'
import axios from 'axios'
import './App.css'

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

function App() {
  const [input, setInput] = useState<string>('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [count, setCount] = useState(0);

  const handleSend = async () => {
    if (!input.trim()) return;

    setMessages((prev) => [...prev, { role: 'user', content: input }]);
    setInput('');

    try {
      const response = await axios.post<{ reply: string }>('http://localhost:5000/chat', {message: input,});

      const reply = response.data.reply;
      setMessages((prev) => [...prev, { role: 'assistant', content: reply}]);
    } catch (error) {
      console.error('Error seding message:', error);
      setMessages((prev) => [...prev, { role: 'assistant', content: 'Failed to get response from AI.' },
      ]);
    }
  };

  function handleClick() {
    setCount(count+1);
  }

  return (
    <div>
      <h1>Free protein</h1>
      <div>
        {messages.map((msg, index) => (<div key={index} style={{textAlign: msg.role === 'user' ? 'right' : 'left', marginBottom: '10px',}}> <strong>{msg.role === 'user' ? 'you': 'AI'}:</strong> {msg.content} </div>))}
      </div>
      <input type="text" value={input} onChange={(e) => setInput(e.target.value)} onKeyPress={(e) => e.key === 'Enter' && handleSend()} style={{ width: '80%', padding: '10px' }} placeholder="Type a message..."/>
      <button onClick={handleSend} style={{ width: '18%', padding: '10px', marginLeft: '2%' }}>
        send
      </button>
    </div>
  );
}

export default App
