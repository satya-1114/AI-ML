import { useEffect, useState } from 'react';

const API_BASE = 'https://ai-ml-ijsm.onrender.com';

function App() {
  const [questions, setQuestions] = useState([]);
  const [selectedQuestion, setSelectedQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const res = await fetch(`${API_BASE}/questions`);
        if (!res.ok) throw new Error('Could not load questions');
        const data = await res.json();
        setQuestions(data);
        if (data.length > 0) setSelectedQuestion(data[0]);
      } catch {
        setError('Unable to connect to backend. Start FastAPI server first.');
      }
    };

    fetchQuestions();
  }, []);

  const handleEvaluate = async () => {
    if (!selectedQuestion || !answer.trim()) {
      setError('Please choose a question and type your answer.');
      return;
    }

    setError('');
    setLoading(true);
    setResult(null);

    try {
      const res = await fetch(`${API_BASE}/evaluate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: selectedQuestion, answer }),
      });

      if (!res.ok) throw new Error('Evaluation failed');
      const data = await res.json();
      setResult(data);
    } catch {
      setError('Failed to evaluate answer. Check backend logs and try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <header className="hero">
        <p className="badge">Interview Prep · AI Powered</p>
        <h1>AI Mock Interview Evaluator</h1>
        <p>
          Get instant feedback on technical interview answers using TF-IDF similarity scoring.
        </p>
      </header>

      <main className="card demo-card">
        <h2>Try the Demo</h2>

        <label htmlFor="question">Interview Question</label>
        <select
          id="question"
          value={selectedQuestion}
          onChange={(e) => setSelectedQuestion(e.target.value)}
        >
          {questions.map((q) => (
            <option key={q} value={q}>
              {q}
            </option>
          ))}
        </select>

        <label htmlFor="answer">Your Answer</label>
        <textarea
          id="answer"
          placeholder="Type your interview answer here..."
          rows={6}
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
        />

        <button onClick={handleEvaluate} disabled={loading}>
          {loading ? 'Evaluating...' : 'Evaluate Answer'}
        </button>

        {error && <p className="error">{error}</p>}

        {result && (
          <section className="result-card">
            <h3>Evaluation Result</h3>
            <div className="result-grid">
              <div>
                <p className="label">Score</p>
                <p className="score">{result.score}/100</p>
              </div>
              <div>
                <p className="label">Status</p>
                <p className={`status ${result.evaluation.toLowerCase().replace(' ', '-')}`}>
                  {result.evaluation}
                </p>
              </div>
            </div>
            <p className="label">Feedback</p>
            <p>{result.feedback}</p>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;
