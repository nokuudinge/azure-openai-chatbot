import { useState } from 'react'
import './App.css'

function App() {
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)

  const sendQuestion = async () => {
    if (loading) return

    const trimmed = question.trim()
    if (!trimmed) {
      setMessages((prev) => [...prev, { role: 'bot', text: 'Please enter a question!' }])
      return
    }

    setMessages((prev) => [...prev, { role: 'user', text: trimmed }])
    setQuestion('')
    setLoading(true)

    try {
      const res = await fetch('http://localhost:8080/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: trimmed }),
      })
      const data = await res.json()
      setMessages((prev) => [...prev, { role: 'bot', text: data.answer }])
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: 'bot', text: 'Sorry, something went wrong. Is the backend running?' },
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="chat">
      <h1>Azure OpenAI Chatbot</h1>

      <div className="messages">
        {messages.length === 0 && (
          <p className="empty">Ask a question to get started.</p>
        )}
        {messages.map((message, i) => (
          <div key={i} className={`message ${message.role}`}>
            {message.text}
          </div>
        ))}
        {loading && <div className="message bot">Thinking…</div>}
      </div>

      <div className="input-row">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && sendQuestion()}
          placeholder="Ask a question..."
        />
        <button onClick={sendQuestion} disabled={loading}>
          Send
        </button>
        <button
          className="clear"
          onClick={() => setMessages([])}
          disabled={loading || messages.length === 0}
        >
          Clear
        </button>
      </div>
    </div>
  )
}

export default App
