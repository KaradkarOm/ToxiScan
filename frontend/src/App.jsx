import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Auto-analyze when text changes (debounced)
  useEffect(() => {
    if (!text.trim()) {
      setResult(null);
      return;
    }

    const timer = setTimeout(() => {
      analyzeText(text);
    }, 500); // Debounce: wait 500ms after user stops typing

    return () => clearTimeout(timer);
  }, [text]);

  const analyzeText = async (textToAnalyze) => {
    if (!textToAnalyze.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/detect`, {
        text: textToAnalyze
      });

      setResult(response.data);
    } catch (err) {
      setError('Unable to connect to the detector service. Is the backend running?');
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const clearText = () => {
    setText('');
    setResult(null);
    setError(null);
  };

  const getSeverityColor = (severity) => {
    const colors = {
      clean: '#10b981',
      low: '#f59e0b',
      medium: '#f97316',
      high: '#dc2626',
      severe: '#7f1d1d'
    };
    return colors[severity] || '#6b7280';
  };

  const getSeverityBg = (severity) => {
    const bgs = {
      clean: '#ecfdf5',
      low: '#fffbeb',
      medium: '#fff7ed',
      high: '#fee2e2',
      severe: '#fef2f2'
    };
    return bgs[severity] || '#f9fafb';
  };

  const getStatusIcon = (severity) => {
    const icons = {
      clean: '✓',
      low: '⚠',
      medium: '⚠',
      high: '✕',
      severe: '✕'
    };
    return icons[severity] || '?';
  };

  return (
    <div className="app">
      <div className="container">
        {/* Header */}
        <header className="header">
          <div className="logo">
            🛡️ Toxicity Detector
          </div>
          <p className="subtitle">Real-time detection of toxic and harmful messages</p>
        </header>

        {/* Main Content */}
        <main className="main-content">
          {/* Input Section */}
          <div className="input-section">
            <label htmlFor="text-input" className="label">
              Enter message to analyze:
            </label>
            <textarea
              id="text-input"
              className="text-input"
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Type or paste your message here..."
              rows="4"
            />
            <div className="input-footer">
              <span className="char-count">{text.length} characters</span>
              {text && (
                <button className="btn btn-clear" onClick={clearText}>
                  Clear
                </button>
              )}
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div className="error-box">
              <strong>Error:</strong> {error}
            </div>
          )}

          {/* Results Section */}
          {result && !loading && (
            <div className="results-section">
              {/* Status Card */}
              <div
                className="status-card"
                style={{ backgroundColor: getSeverityBg(result.severity) }}
              >
                <div className="status-header">
                  <div className="status-icon" style={{ color: getSeverityColor(result.severity) }}>
                    {getStatusIcon(result.severity)}
                  </div>
                  <div className="status-text">
                    <span className="status-label">
                      {result.is_toxic ? 'TOXIC' : 'CLEAN'}
                    </span>
                    <span className="status-severity" style={{ color: getSeverityColor(result.severity) }}>
                      {result.severity.toUpperCase()}
                    </span>
                  </div>
                </div>

                {/* Toxicity Score Bar */}
                <div className="score-section">
                  <div className="score-header">
                    <span>Toxicity Score</span>
                    <span className="score-value">{(result.toxicity_score * 100).toFixed(0)}%</span>
                  </div>
                  <div className="progress-bar">
                    <div
                      className="progress-fill"
                      style={{
                        width: `${result.toxicity_score * 100}%`,
                        backgroundColor: getSeverityColor(result.severity)
                      }}
                    />
                  </div>
                </div>
              </div>

              {/* Toxic Words Section */}
              {result.toxic_words && result.toxic_words.length > 0 && (
                <div className="toxic-words-section">
                  <h3 className="section-title">Toxic Words Detected</h3>
                  <div className="toxic-words-list">
                    {result.toxic_words.map((word, index) => (
                      <span key={index} className="toxic-word-badge">
                        {word[0]}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Reasons Section */}
              <div className="reasons-section">
                <h3 className="section-title">Why This Classification?</h3>
                <ul className="reasons-list">
                  {result.reasons.map((reason, index) => (
                    <li key={index} className="reason-item">
                      <span className="reason-bullet">•</span>
                      {reason}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Sentiment Analysis Section */}
              <div className="sentiment-section">
                <h3 className="section-title">Sentiment Analysis</h3>
                <div className="sentiment-grid">
                  <div className="sentiment-item">
                    <span className="sentiment-label">Negative</span>
                    <div className="sentiment-bar">
                      <div
                        className="sentiment-fill negative"
                        style={{ width: `${result.sentiment_scores.neg * 100}%` }}
                      />
                    </div>
                    <span className="sentiment-value">{(result.sentiment_scores.neg * 100).toFixed(0)}%</span>
                  </div>
                  <div className="sentiment-item">
                    <span className="sentiment-label">Neutral</span>
                    <div className="sentiment-bar">
                      <div
                        className="sentiment-fill neutral"
                        style={{ width: `${result.sentiment_scores.neu * 100}%` }}
                      />
                    </div>
                    <span className="sentiment-value">{(result.sentiment_scores.neu * 100).toFixed(0)}%</span>
                  </div>
                  <div className="sentiment-item">
                    <span className="sentiment-label">Positive</span>
                    <div className="sentiment-bar">
                      <div
                        className="sentiment-fill positive"
                        style={{ width: `${result.sentiment_scores.pos * 100}%` }}
                      />
                    </div>
                    <span className="sentiment-value">{(result.sentiment_scores.pos * 100).toFixed(0)}%</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Loading State */}
          {loading && (
            <div className="loading-section">
              <div className="spinner" />
              <p>Analyzing...</p>
            </div>
          )}

          {/* Empty State */}
          {!result && !loading && !error && (
            <div className="empty-state">
              <p className="empty-icon">💬</p>
              <p className="empty-text">Start typing to analyze text for toxicity</p>
            </div>
          )}
        </main>

        {/* Footer */}
        <footer className="footer">
          <p>🛡️ Toxicity & Cyberbullying Detector | Built with ❤️</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
