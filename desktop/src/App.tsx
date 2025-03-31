import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [question, setQuestion] = useState('');
  const [ws, setWs] = useState<WebSocket | null>(null);

  useEffect(() => {
    const websocket = new WebSocket('ws://localhost:8000/ws/123');
    setWs(websocket);

    return () => {
      websocket.close();
    };
  }, []);

  const handleSendQuestion = () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ question }));
      setQuestion('');
    }
  };

  return (
      <div>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Enter your question"
        />
        <button type='button' onClick={() => handleSendQuestion()}>Send</button>
      </div>
  )
}

export default App
