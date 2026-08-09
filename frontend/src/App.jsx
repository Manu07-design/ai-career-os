import { useState } from "react";
import ReactMarkdown from "react-markdown";
import "./App.css";

const API = "http://127.0.0.1:8000";

function App() {
  const [file, setFile] = useState(null);
  const [targetRole, setTargetRole] = useState("AI Engineer");

  const [uploadResult, setUploadResult] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [roadmap, setRoadmap] = useState("");
  const [question, setQuestion] = useState("");
  const [chatAnswer, setChatAnswer] = useState("");
  const [chatSources, setChatSources] = useState([]);

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [activeAction, setActiveAction] = useState("");

  // --------------------------------------------------
  // Helpers
  // --------------------------------------------------

  function getScoreColor(score) {
    if (score >= 80) return "#22c55e";
    if (score >= 60) return "#f59e0b";
    return "#ef4444";
  }

  function getScoreLabel(score) {
    if (score >= 85) return "Excellent";
    if (score >= 70) return "Strong";
    if (score >= 50) return "Developing";
    return "Needs Improvement";
  }

  function clearMessage() {
    setMessage("");
  }

  // --------------------------------------------------
  // Resume Upload
  // --------------------------------------------------

  async function uploadResume() {
    if (!file) {
      setMessage("Please select a PDF resume first.");
      return;
    }

    if (!file.name.toLowerCase().endsWith(".pdf")) {
      setMessage("Only PDF resumes are supported.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      setActiveAction("upload");
      setMessage("");

      const response = await fetch(`${API}/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Resume upload failed.");
      }

      setUploadResult(data);

      // Reset downstream results because a new resume was uploaded.
      setAnalysis(null);
      setRoadmap("");
      setChatAnswer("");
      setChatSources([]);

      setMessage("Resume uploaded and indexed successfully.");
    } catch (error) {
      setMessage(error.message || "Unable to upload resume.");
    } finally {
      setLoading(false);
      setActiveAction("");
    }
  }

  // --------------------------------------------------
  // Career Gap Analysis
  // --------------------------------------------------

  async function analyzeCareer() {
    if (!uploadResult) {
      setMessage("Upload your resume before analyzing career readiness.");
      return;
    }

    try {
      setLoading(true);
      setActiveAction("analysis");
      setMessage("");

      const response = await fetch(
        `${API}/analyze?target_role=${encodeURIComponent(targetRole)}`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Career analysis failed.");
      }

      setAnalysis(data);
      setMessage("Career readiness analysis completed.");
    } catch (error) {
      setMessage(error.message || "Unable to analyze career readiness.");
    } finally {
      setLoading(false);
      setActiveAction("");
    }
  }

  // --------------------------------------------------
  // Roadmap
  // --------------------------------------------------

  async function generateRoadmap() {
    if (!uploadResult) {
      setMessage("Upload your resume before generating a roadmap.");
      return;
    }

    try {
      setLoading(true);
      setActiveAction("roadmap");
      setMessage("");

      const response = await fetch(
        `${API}/roadmap?target_role=${encodeURIComponent(targetRole)}`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Roadmap generation failed.");
      }

      setRoadmap(data.roadmap || "");
      setMessage("Personalized roadmap generated.");
    } catch (error) {
      setMessage(error.message || "Unable to generate roadmap.");
    } finally {
      setLoading(false);
      setActiveAction("");
    }
  }

  // --------------------------------------------------
  // Resume-Aware RAG Chat
  // --------------------------------------------------

  async function askResume(customQuestion = null) {
    const finalQuestion =
      customQuestion !== null ? customQuestion : question;

    if (!finalQuestion.trim()) {
      setMessage("Enter a question about your resume.");
      return;
    }

    if (!uploadResult) {
      setMessage("Upload your resume before using Resume-Aware AI.");
      return;
    }

    try {
      setLoading(true);
      setActiveAction("chat");
      setMessage("");

      const response = await fetch(
        `${API}/chat?question=${encodeURIComponent(
          finalQuestion
        )}&top_k=3`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Chat request failed.");
      }

      setQuestion(finalQuestion);
      setChatAnswer(data.answer || "");
      setChatSources(data.sources || []);
    } catch (error) {
      setMessage(error.message || "Unable to answer your question.");
    } finally {
      setLoading(false);
      setActiveAction("");
    }
  }

  // --------------------------------------------------
  // Suggested Questions
  // --------------------------------------------------

  function askSuggestedQuestion(text) {
    setQuestion(text);
    askResume(text);
  }

  // --------------------------------------------------
  // Loading text
  // --------------------------------------------------

  function getLoadingText() {
    if (activeAction === "upload") return "Indexing your resume...";
    if (activeAction === "analysis") return "Analyzing career readiness...";
    if (activeAction === "roadmap") return "Building your learning roadmap...";
    if (activeAction === "chat") return "Searching your resume...";
    return "AI is working...";
  }

  const readinessScore = analysis?.readiness_score ?? 0;

  return (
    <div className="app">
      {/* ==================================================
          HEADER
      ================================================== */}

      <header className="hero">
        <div className="hero-content">
          <div className="brand-row">
            <div className="brand-icon">AI</div>

            <span className="eyebrow">
              PERSONAL CAREER INTELLIGENCE
            </span>
          </div>

          <h1>AI Career OS</h1>

          <p className="hero-description">
            Turn your resume into an intelligent career strategy.
            Analyze your skills, discover gaps, build a learning
            roadmap, and chat with your resume using RAG.
          </p>

          <div className="hero-tags">
            <span>RAG</span>
            <span>FAISS</span>
            <span>Embeddings</span>
            <span>AI Agents</span>
          </div>
        </div>

        <div className="hero-status">
          <span className="status-dot"></span>
          AI SYSTEM ONLINE
        </div>
      </header>

      {/* ==================================================
          GLOBAL MESSAGE
      ================================================== */}

      {message && (
        <div className="message">
          <span className="message-icon">✓</span>
          <span>{message}</span>

          <button
            className="message-close"
            onClick={clearMessage}
            aria-label="Close message"
          >
            ×
          </button>
        </div>
      )}

      {/* ==================================================
          MAIN DASHBOARD
      ================================================== */}

      <main>
        {/* ==================================================
            01 — RESUME INTELLIGENCE
        ================================================== */}

        <section className="card resume-card">
          <div className="section-header">
            <div className="section-number">01</div>

            <div>
              <div className="section-label">
                RESUME INTELLIGENCE
              </div>

              <h2>Build Your Career Profile</h2>
            </div>
          </div>

          <p className="muted">
            Upload your resume to extract skills, create semantic
            embeddings, and build your personal career knowledge base.
          </p>

          <div className="upload-zone">
            <div className="upload-icon">↑</div>

            <h3>
              {file ? file.name : "Upload your resume"}
            </h3>

            <p>
              PDF format · Your resume powers the entire AI system
            </p>

            <label className="file-button">
              Choose PDF
              <input
                type="file"
                accept=".pdf,application/pdf"
                onChange={(e) => {
                  setFile(e.target.files[0] || null);
                  setMessage("");
                }}
              />
            </label>
          </div>

          <button
            className="primary-button full-width"
            onClick={uploadResume}
            disabled={loading}
          >
            {activeAction === "upload"
              ? "Indexing Resume..."
              : "Upload & Analyze Resume"}
          </button>

          {uploadResult && (
            <div className="result">
              <div className="result-title-row">
                <h3>Skills Extracted</h3>

                <span className="success-pill">
                  ✓ Indexed
                </span>
              </div>

              {uploadResult.skills &&
              uploadResult.skills.length > 0 ? (
                <div className="skills">
                  {uploadResult.skills.map((skill) => (
                    <span className="skill-badge" key={skill}>
                      {skill}
                    </span>
                  ))}
                </div>
              ) : (
                <div className="empty-state">
                  No recognized skills were extracted from this
                  resume.
                </div>
              )}

              {uploadResult.vector_store && (
                <div className="vector-info">
                  <div className="vector-icon">◆</div>

                  <div>
                    <strong>
                      {
                        uploadResult.vector_store
                          .vectors_stored
                      }{" "}
                      vectors indexed
                    </strong>

                    <p>
                      Resume content is now searchable through
                      FAISS semantic retrieval.
                    </p>
                  </div>
                </div>
              )}
            </div>
          )}
        </section>

        {/* ==================================================
            02 — CAREER GAP ANALYSIS
        ================================================== */}

        <section className="card">
          <div className="section-header">
            <div className="section-number">02</div>

            <div>
              <div className="section-label">
                CAREER GAP ANALYSIS
              </div>

              <h2>Measure Your Readiness</h2>
            </div>
          </div>

          <p className="muted">
            Compare your current skills against the requirements
            of your target role.
          </p>

          <label className="field-label">
            Target Career
          </label>

          <select
            value={targetRole}
            onChange={(e) => {
              setTargetRole(e.target.value);
              setAnalysis(null);
              setRoadmap("");
            }}
          >
            <option>AI Engineer</option>
            <option>ML Engineer</option>
            <option>Data Scientist</option>
            <option>Frontend Developer</option>
          </select>

          <button
            className="primary-button full-width"
            onClick={analyzeCareer}
            disabled={loading}
          >
            {activeAction === "analysis"
              ? "Analyzing..."
              : "Analyze Career Readiness"}
          </button>

          {analysis && (
            <div className="result">
              <div className="score-card">
                <div>
                  <span className="score-label">
                    READINESS SCORE
                  </span>

                  <div
                    className="score"
                    style={{
                      color: getScoreColor(
                        readinessScore
                      ),
                    }}
                  >
                    {readinessScore}%
                  </div>

                  <span
                    className="score-status"
                    style={{
                      color: getScoreColor(
                        readinessScore
                      ),
                    }}
                  >
                    {getScoreLabel(readinessScore)}
                  </span>
                </div>

                <div className="score-ring">
                  <div
                    className="score-ring-progress"
                    style={{
                      background: `conic-gradient(
                        ${getScoreColor(
                          readinessScore
                        )} ${readinessScore * 3.6}deg,
                        #1f2937 ${readinessScore * 3.6}deg
                      )`,
                    }}
                  >
                    <div className="score-ring-inner">
                      {readinessScore}
                    </div>
                  </div>
                </div>
              </div>

              <div className="analysis-section">
                <h3>Missing Skills</h3>

                {analysis.missing_skills &&
                analysis.missing_skills.length > 0 ? (
                  <div className="skills">
                    {analysis.missing_skills.map(
                      (skill) => (
                        <span
                          className="missing-skill"
                          key={skill}
                        >
                          + {skill}
                        </span>
                      )
                    )}
                  </div>
                ) : (
                  <div className="success-box">
                    Excellent. No major skill gaps detected.
                  </div>
                )}
              </div>
            </div>
          )}
        </section>

        {/* ==================================================
            03 — ROADMAP
        ================================================== */}

        <section className="card roadmap-card">
          <div className="section-header">
            <div className="section-number">03</div>

            <div>
              <div className="section-label">
                AI CAREER PLANNER
              </div>

              <h2>Your Learning Roadmap</h2>
            </div>
          </div>

          <p className="muted">
            Generate a personalized learning plan based on your
            current skills, missing skills, and target role.
          </p>

          <div className="roadmap-meta">
            <span>
              Target: <strong>{targetRole}</strong>
            </span>

            {analysis && (
              <span>
                Readiness:{" "}
                <strong>{readinessScore}%</strong>
              </span>
            )}
          </div>

          <button
            className="primary-button"
            onClick={generateRoadmap}
            disabled={loading}
          >
            {activeAction === "roadmap"
              ? "Generating Roadmap..."
              : "Generate AI Roadmap"}
          </button>

          {roadmap && (
            <div className="roadmap">
              <ReactMarkdown>
                {roadmap}
              </ReactMarkdown>
            </div>
          )}

          {!roadmap && (
            <div className="roadmap-placeholder">
              <div className="placeholder-icon">✦</div>

              <h3>Your personalized roadmap will appear here</h3>

              <p>
                Upload your resume and analyze your career
                readiness first.
              </p>
            </div>
          )}
        </section>

        {/* ==================================================
            04 — RAG CHAT
        ================================================== */}

        <section className="card chat-card">
          <div className="section-header">
            <div className="section-number">04</div>

            <div>
              <div className="section-label">
                RETRIEVAL-AUGMENTED AI
              </div>

              <h2>Resume-Aware AI Chat</h2>
            </div>
          </div>

          <p className="muted">
            Ask questions about your resume. The system retrieves
            relevant resume evidence before generating an answer.
          </p>

          <div className="chat-window">
            {!chatAnswer ? (
              <div className="chat-empty">
                <div className="chat-ai-icon">AI</div>

                <h3>Ask your career knowledge base</h3>

                <p>
                  Your questions are answered using evidence
                  retrieved from your uploaded resume.
                </p>
              </div>
            ) : (
              <div className="chat-response">
                <div className="response-header">
                  <div className="chat-ai-icon small">
                    AI
                  </div>

                  <div>
                    <strong>AI Career Advisor</strong>
                    <span>Resume-grounded response</span>
                  </div>
                </div>

                <div className="answer">
                  {chatAnswer}
                </div>

                {chatSources.length > 0 && (
                  <div className="sources">
                    <h4>Retrieved Evidence</h4>

                    {chatSources.map((source, index) => (
                      <div
                        className="source-card"
                        key={index}
                      >
                        <span>
                          Source {index + 1}
                        </span>

                        <p>
                          {typeof source === "string"
                            ? source
                            : source.text ||
                              source.content ||
                              JSON.stringify(source)}
                        </p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>

          <div className="suggested-title">
            Suggested questions
          </div>

          <div className="suggested-questions">
            <button
              onClick={() =>
                askSuggestedQuestion(
                  "Summarize my resume"
                )
              }
              disabled={loading}
            >
              Summarize Resume
            </button>

            <button
              onClick={() =>
                askSuggestedQuestion(
                  "What are my strongest skills?"
                )
              }
              disabled={loading}
            >
              Strongest Skills
            </button>

            <button
              onClick={() =>
                askSuggestedQuestion(
                  "What projects have I completed?"
                )
              }
              disabled={loading}
            >
              My Projects
            </button>

            <button
              onClick={() =>
                askSuggestedQuestion(
                  "What should I learn next?"
                )
              }
              disabled={loading}
            >
              What Should I Learn?
            </button>
          </div>

          <div className="chat-input">
            <input
              value={question}
              placeholder="Ask something about your resume..."
              onChange={(e) =>
                setQuestion(e.target.value)
              }
              onKeyDown={(e) => {
                if (e.key === "Enter" && !loading) {
                  askResume();
                }
              }}
            />

            <button
              className="ask-button"
              onClick={() => askResume()}
              disabled={loading || !question.trim()}
            >
              {activeAction === "chat"
                ? "..."
                : "Ask AI"}
            </button>
          </div>
        </section>
      </main>

      {/* ==================================================
          FOOTER
      ================================================== */}

      <footer className="footer">
        <div>
          <strong>AI Career OS</strong>

          <span>
            Resume intelligence platform
          </span>
        </div>

        <div className="footer-tech">
          <span>FastAPI</span>
          <span>React</span>
          <span>FAISS</span>
          <span>Embeddings</span>
          <span>RAG</span>
          <span>AI Agents</span>
        </div>
      </footer>

      {/* ==================================================
          GLOBAL LOADING INDICATOR
      ================================================== */}

      {loading && (
        <div className="loading">
          <div className="spinner"></div>

          <div>
            <strong>{getLoadingText()}</strong>
            <span>Please wait...</span>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;