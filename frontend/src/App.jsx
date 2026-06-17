import { useState, useRef, useEffect } from "react";

// ─── CONFIG ───────────────────────────────────────────────────────────────────
const BACKEND_URL = "http://localhost:8000";

// ─── SUGGESTION CHIPS ─────────────────────────────────────────────────────────
const SUGGESTIONS = [
  "Explain quantum computing simply",
  "Write a Python fibonacci function",
  "Best practices for REST APIs",
  "What is the CAP theorem?",
];

// ─── TYPING DOTS ──────────────────────────────────────────────────────────────
function TypingDots() {
  return (
    <div style={{ display: "flex", gap: 4, alignItems: "center", padding: "4px 0" }}>
      {[0, 1, 2].map((i) => (
        <div key={i} style={{
          width: 6, height: 6, borderRadius: "50%", background: "#555",
          animation: `pulse 1.2s ease-in-out ${i * 0.2}s infinite`,
        }} />
      ))}
    </div>
  );
}

// ─── CHUNK PANEL ──────────────────────────────────────────────────────────────
function ChunkPanel({ chunks, isOpen, onClose,theme}) {
  if (!isOpen || !chunks?.length) return null;
  return (
    <div style={{
      position: "fixed", right: 0, top: 0, bottom: 0, width: 340,
      background: "#0f0f0f", borderLeft: "1px solid #1e1e1e",
      display: "flex", flexDirection: "column", zIndex: 50,
      animation: "slideIn 0.22s ease forwards",
    }}>
      {/* Header */}
      <div style={{
        padding: "14px 16px", borderBottom: "1px solid #1a1a1a",
        display: "flex", alignItems: "center", gap: 8, flexShrink: 0,
      }}>
        <span style={{ fontFamily: "'IBM Plex Mono', monospace", fontSize: 10, color: "#555", letterSpacing: "0.18em", flex: 1 }}>
          RETRIEVED CHUNKS · {chunks.length}
        </span>
        <button onClick={onClose} style={{
          background: "transparent", border: "1px solid #1e1e1e", borderRadius: 4,
          padding: "3px 8px", fontSize: 10, color: "#444", cursor: "pointer",
          fontFamily: "'IBM Plex Mono', monospace",
        }}>✕</button>
      </div>
      {/* Chunks */}
      <div style={{ flex: 1, overflowY: "auto", padding: "12px 14px", display: "flex", flexDirection: "column", gap: 10 }}>
        {chunks.map((chunk, i) => (
          <div key={i} style={{
            background: theme.text, border: "1px solid #1e1e1e",
            borderRadius: 8, padding: "10px 12px",
          }}>
            <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 6 }}>
              <span style={{
                fontFamily: "'IBM Plex Mono', monospace", fontSize: 9,
                background: "#1a1a3a", color: "#7b8cde", padding: "2px 7px",
                borderRadius: 3, letterSpacing: "0.1em",
              }}>#{i + 1}</span>
              {chunk.source && (
                <span style={{
                  fontFamily: "'IBM Plex Mono', monospace", fontSize: 9,
                  color: "#c8a96e", overflow: "hidden", textOverflow: "ellipsis",
                  whiteSpace: "nowrap", maxWidth: 220,
                }}>{chunk.source}</span>
              )}
              {chunk.score != null && (
                <span style={{
                  marginLeft: "auto", fontFamily: "'IBM Plex Mono', monospace",
                  fontSize: 9, color: "#2a5a2a",
                  background: "#0a1a0a", padding: "2px 6px", borderRadius: 3,
                }}>
                  {(chunk.score * 100).toFixed(0)}%
                </span>
              )}
            </div>
            <div style={{
              fontSize: 11.5, color: "#666", lineHeight: 1.65,
              fontFamily: "'IBM Plex Sans', sans-serif", fontWeight: 300,
            }}>
              {chunk.text}
            </div>
            {chunk.page != null && (
              <div style={{ marginTop: 6, fontSize: 9, color: "#333", fontFamily: "'IBM Plex Mono', monospace" }}>
                page {chunk.page}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── CITATION BADGE ───────────────────────────────────────────────────────────
function CitationBadge({ citation, index }) {
  const [hover, setHover] = useState(false);
  return (
    <span style={{ position: "relative", display: "inline-block" }}>
      <span
        onMouseEnter={() => setHover(true)}
        onMouseLeave={() => setHover(false)}
        style={{
          display: "inline-flex", alignItems: "center", justifyContent: "center",
          width: 16, height: 16, borderRadius: "50%",
          background: "#1a1a3a", border: "1px solid #3a3a6a",
          color: "#7b8cde", fontSize: 9, fontFamily: "'IBM Plex Mono', monospace",
          cursor: "pointer", verticalAlign: "super", marginLeft: 2,
          fontWeight: 600, lineHeight: 1,
        }}
      >
        {index + 1}
      </span>
      {hover && citation && (
        <div style={{
          position: "absolute", bottom: "calc(100% + 6px)", left: "50%",
          transform: "translateX(-50%)", width: 220,
          background: "#141414", border: "1px solid #2a2a5a",
          borderRadius: 8, padding: "8px 10px", zIndex: 100,
          boxShadow: "0 8px 24px rgba(0,0,0,0.6)",
          pointerEvents: "none",
        }}>
          <div style={{ fontSize: 9, color: "#c8a96e", fontFamily: "'IBM Plex Mono', monospace", marginBottom: 4 }}>
            {citation.source}
          </div>
          <div style={{ fontSize: 11, color: "#888", lineHeight: 1.5, fontFamily: "'IBM Plex Sans', sans-serif" }}>
            {citation.text?.slice(0, 140)}{citation.text?.length > 140 ? "…" : ""}
          </div>
          {citation.page != null && (
            <div style={{ marginTop: 4, fontSize: 9, color: "#444", fontFamily: "'IBM Plex Mono', monospace" }}>
              page {citation.page}
            </div>
          )}
        </div>
      )}
    </span>
  );
}

// ─── INLINE CITATION RENDERER ─────────────────────────────────────────────────
// Looks for [1], [2] markers in content and replaces with badge components
function renderWithCitations(content, citations) {
  if (!citations?.length) return content;
  const parts = content.split(/(\[\d+\])/g);
  return parts.map((part, i) => {
    const match = part.match(/^\[(\d+)\]$/);
    if (match) {
      const idx = parseInt(match[1], 10) - 1;
      const citation = citations[idx];
      return <CitationBadge key={i} citation={citation} index={idx} />;
    }
    return part;
  });
}

// ─── SOURCE LIST ──────────────────────────────────────────────────────────────
function SourceList({ citations,theme }) {
  if (!citations?.length) return null;
  const unique = Array.from(new Map(citations.map((c) => [c.source, c])).values());
  return (
    <div style={{ marginTop: 10, paddingTop: 10, borderTop: "1px solid #1e1e1e" }}>
      <div style={{
        fontFamily: "'IBM Plex Mono', monospace", fontSize: 9,
        color: theme.text, letterSpacing: "0.15em", marginBottom: 6,
      }}>SOURCES</div>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 5 }}>
        {unique.map((c, i) => (
          <span key={i} style={{
            background: "#0d0d1a", border: "1px solid #2a2a4a",
            borderRadius: 4, padding: "3px 8px",
            fontSize: 10, color: "#7b8cde",
            fontFamily: "'IBM Plex Mono', monospace",
            display: "flex", alignItems: "center", gap: 5,
          }}>
            <svg width="8" height="8" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
            {c.source}
          </span>
        ))}
      </div>
    </div>
  );
}

// ─── MESSAGE BUBBLE ───────────────────────────────────────────────────────────
function MessageBubble({ msg, onShowChunks,theme }) {
  const isUser = msg.role === "user";
  const hasCitations = msg.citations?.length > 0;
  const hasChunks = msg.chunks?.length > 0;

  return (
    <div style={{
      display: "flex",
      flexDirection: isUser ? "row-reverse" : "row",
      alignItems: "flex-start",
      gap: 10,
      marginBottom: 20,
      animation: "fadeUp 0.28s ease forwards",
    }}>
      {/* Avatar */}
      <div style={{
        width: 30, height: 30, borderRadius: "50%", flexShrink: 0,
        background: isUser ? "#1a1a2e" : "#1a1a1a",
        border: isUser ? "1px solid #3a3a6a" : "1px solid #2a2a2a",
        display: "flex", alignItems: "center", justifyContent: "center",
        fontSize: 12, fontFamily: "'IBM Plex Mono', monospace",
        color: isUser ? "#7b8cde" : "#c8a96e", fontWeight: 600,
      }}>
        {isUser ? "U" : "✦"}
      </div>

      {/* Bubble */}
      <div style={{
        maxWidth: "78%",
        background: isUser ? "#12122a" : "#141414",
        border: isUser ? "1px solid #2a2a5a" : "1px solid #222",
        borderRadius: isUser ? "16px 4px 16px 16px" : "4px 16px 16px 16px",
        padding: "11px 15px",
        color: isUser ? "#c8ccf5" : "#e0d9cc",
        fontSize: 13.5, lineHeight: 1.75, fontWeight: 300,
        wordBreak: "break-word",
      }}>
        <div style={{ whiteSpace: "pre-wrap" }}>
          {hasCitations ? renderWithCitations(msg.content, msg.citations) : msg.content}
          {msg.streaming && (
            <span style={{
              display: "inline-block", width: 2, height: 14,
              background: "#e8e0d0", marginLeft: 2, verticalAlign: "middle",
              animation: "blink 0.9s step-end infinite",
            }} />
          )}
        </div>

        {/* Source list */}
        {!isUser && hasCitations && !msg.streaming && <SourceList citations={msg.citations} theme={theme}/>}

        {/* Chunks button */}
        {!isUser && hasChunks && !msg.streaming && (
          <button onClick={() => onShowChunks(msg.chunks)} style={{
            marginTop: 10, background: "transparent",
            border: "1px solid #1e1e1e", borderRadius: 5,
            padding: "4px 10px", fontSize: 10, color: "#444",
            cursor: "pointer", fontFamily: "'IBM Plex Mono', monospace",
            letterSpacing: "0.1em", display: "flex", alignItems: "center", gap: 5,
            transition: "border-color 0.15s, color 0.15s",
          }}
            onMouseEnter={(e) => { e.currentTarget.style.borderColor = "#333"; e.currentTarget.style.color = "#888"; }}
            onMouseLeave={(e) => { e.currentTarget.style.borderColor = "#1e1e1e"; e.currentTarget.style.color = "#444"; }}
          >
            <svg width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"><rect x="2" y="3" width="20" height="4"/><rect x="2" y="10" width="20" height="4"/><rect x="2" y="17" width="20" height="4"/></svg>
            VIEW {msg.chunks.length} CHUNKS
          </button>
        )}
      </div>
    </div>
  );
}

// ─── FILE UPLOAD AREA ─────────────────────────────────────────────────────────
function FileUploadArea({ uploadedFiles, onUpload, onRemove,theme }) {
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const inputRef = useRef(null);

  const ACCEPTED = [".pdf", ".txt", ".md", ".docx", ".csv"];
  const ACCEPTED_MIME = ["application/pdf", "text/plain", "text/markdown", "text/csv",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"];

  const isValidFile = (f) => {
    return ACCEPTED_MIME.includes(f.type) || ACCEPTED.some((ext) => f.name.endsWith(ext));
  };

  const handleFiles = async (files) => {
    setError(null);
    const valid = Array.from(files).filter(isValidFile);
    const invalid = Array.from(files).filter((f) => !isValidFile(f));
    if (invalid.length) setError(`Unsupported: ${invalid.map((f) => f.name).join(", ")}`);
    if (!valid.length) return;

    setUploading(true);
    try {
      const formData = new FormData();
      valid.forEach((f) => formData.append("files", f));
      const res = await fetch(`${BACKEND_URL}/upload`, { method: "POST", body: formData });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      onUpload(data.files || valid.map((f) => ({ name: f.name, size: f.size })));
    } catch (e) {
      // Optimistic fallback — show file locally even if backend unavailable
      onUpload(valid.map((f) => ({ name: f.name, size: f.size, local: true })));
    }
    setUploading(false);
  };

  const onDrop = (e) => {
    e.preventDefault(); setDragging(false);
    handleFiles(e.dataTransfer.files);
  };

  const fmt = (bytes) => bytes < 1024 ? `${bytes}B` : bytes < 1048576 ? `${(bytes / 1024).toFixed(0)}KB` : `${(bytes / 1048576).toFixed(1)}MB`;

  return (
    <div style={{ marginBottom: 10 }}>
      {/* Drop zone */}
      <div
        onDragEnter={() => setDragging(true)}
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
        onClick={() => inputRef.current?.click()}
        style={{
          border: `1px dashed ${dragging ? "#c8a96e" : "#222"}`,
          borderRadius: 10, padding: "14px 16px",
          cursor: "pointer", transition: "border-color 0.15s, background 0.15s",
          background: dragging ? "#141200" : "#0d0d0d",
          display: "flex", alignItems: "center", gap: 12,
        }}
        onMouseEnter={(e) => { if (!dragging) e.currentTarget.style.borderColor = "#333"; }}
        onMouseLeave={(e) => { if (!dragging) e.currentTarget.style.borderColor = "#222"; }}
      >
        <input ref={inputRef} type="file" multiple accept={ACCEPTED.join(",")}
          style={{ display: "none" }} onChange={(e) => handleFiles(e.target.files)} />
        <div style={{
          width: 32, height: 32, borderRadius: 8, background: "#141414",
          border: "1px solid #222", display: "flex", alignItems: "center",
          justifyContent: "center", flexShrink: 0,
        }}>
          {uploading
            ? <div style={{ width: 14, height: 14, border: "2px solid #222", borderTop: "2px solid #c8a96e", borderRadius: "50%", animation: "spin 0.8s linear infinite" }} />
            : <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#555" strokeWidth="2" strokeLinecap="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
          }
        </div>
        <div>
          <div style={{ fontSize: 11.5, color: "#555", fontFamily: "'IBM Plex Sans', sans-serif" }}>
            {dragging ? "Drop files here" : "Upload documents to ground answers"}
          </div>
          <div style={{ fontSize: 9.5, color: "#2a2a2a", fontFamily: "'IBM Plex Mono', monospace", marginTop: 2, letterSpacing: "0.08em" }}>
            PDF · TXT · MD · DOCX · CSV
          </div>
        </div>
      </div>

      {/* Error */}
      {error && (
        <div style={{ marginTop: 5, fontSize: 10, color: "#8a3a3a", fontFamily: "'IBM Plex Mono', monospace" }}>
          {error}
        </div>
      )}

      {/* File pills */}
      {uploadedFiles.length > 0 && (
        <div style={{ marginTop: 7, display: "flex", flexWrap: "wrap", gap: 5 }}>
          {uploadedFiles.map((f, i) => (
            <div key={i} style={{
              background: theme.card, border: `1px solid ${theme.border}`,
              borderRadius: 5, padding: "4px 8px 4px 10px",
              display: "flex", alignItems: "center", gap: 6,
              fontSize: 10, color: "#666", fontFamily: "'IBM Plex Mono', monospace",
            }}>
              <svg width="8" height="8" viewBox="0 0 24 24" fill="none" stroke={f.local ? "#555" : "#c8a96e"} strokeWidth="2.5" strokeLinecap="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
              </svg>
              <span style={{ maxWidth: 140, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{f.name}</span>
              {f.size && <span style={{ color: "#2a2a2a" }}>{fmt(f.size)}</span>}
              {f.local && <span style={{ color: "#444", fontSize: 8 }}>LOCAL</span>}
              <button onClick={(e) => { e.stopPropagation(); onRemove(i); }} style={{
                background: "transparent", border: "none", cursor: "pointer",
                color: "#333", padding: "0 2px", fontSize: 12, lineHeight: 1,
                display: "flex", alignItems: "center",
              }}
                onMouseEnter={(e) => (e.currentTarget.style.color = "#888")}
                onMouseLeave={(e) => (e.currentTarget.style.color = "#333")}
              >×</button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// ─── MAIN APP ─────────────────────────────────────────────────────────────────
export default function App() {
  const [messages, setMessages]         = useState([]);
  const [input, setInput]               = useState("");
  const [darkMode, setDarkMode] = useState(true);
  const theme = {
  background: darkMode ? "#0d0d0d" : "#f5f5f5",
  text: darkMode ? "#e0d9cc" : "#1a1a1a",
  card: darkMode ? "#141414" : "#ffffff",
  border: darkMode ? "#1a1a1a" : "#d1d5db",
  secondary: darkMode ? "#555" : "#4b5563",
};
  const [loading, setLoading]           = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [chunkPanel, setChunkPanel]     = useState({ open: false, chunks: [] });
  const [showUpload, setShowUpload]     = useState(false);
  const bottomRef = useRef(null);
  const taRef     = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // ── Call FastAPI /analyze ──────────────────────────────────────────────────
  // Now expects: { reply, citations?, chunks? }
  // citations: [{ source, text, page? }]
  // chunks:    [{ source, text, score?, page? }]
const fetchReply = async (text) => {

  const hasDocument = uploadedFiles.length > 0;

  const endpoint = hasDocument
    ? `${BACKEND_URL}/document-chat`
    : `${BACKEND_URL}/chat`;

  const res = await fetch(endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query: text,
      has_document: hasDocument,
      top_k: 3,
      rerank_top_n: 3,
      use_reranker: false,
    }),
  });

  if (!res.ok) {
    throw new Error(`HTTP ${res.status}`);
  }
  return res.json();
};
  // ── Send handler ───────────────────────────────────────────────────────────
  const handleSend = async (text) => {
    const query = (text || input).trim();
    if (!query || loading) return;

    const userId      = Date.now();
    const assistantId = Date.now() + 1;

    setMessages((prev) => [
      ...prev,
      { id: userId,      role: "user",      content: query },
      { id: assistantId, role: "assistant", content: "", streaming: true },
    ]);
    setInput("");
    setLoading(true);

    try {
      const data = await fetchReply(query);
   setMessages((prev) =>
  prev.map((m) =>
    m.id === assistantId
      ? {
          ...m,
          content: data.answer || data.reply,
          citations: data.citations || [],
          chunks: data.chunks || [],
          streaming: false,
        }
      : m
  )
);
    } catch (e) {
      setMessages((prev) =>
        prev.map((m) =>
          m.id === assistantId
            ? { ...m, content: `Error: ${e.message}. Is the backend running on ${BACKEND_URL}?`, streaming: false }
            : m
        )
      );
    }

    setLoading(false);
    setTimeout(() => taRef.current?.focus(), 50);
  };

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSend(); }
  };

  const clearChat = () => { setMessages([]); setInput(""); };
  const isEmpty   = messages.length === 0;

  const hasFiles  = uploadedFiles.length > 0;

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        ::-webkit-scrollbar { width: 3px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #2a2a2a; border-radius: 2px; }
        @keyframes fadeUp  { from { opacity:0; transform:translateY(10px); } to { opacity:1; transform:translateY(0); } }
        @keyframes blink   { 0%,100%{opacity:1} 50%{opacity:0} }
        @keyframes pulse   { 0%,100%{transform:scale(1)} 50%{transform:scale(1.15)} }
        @keyframes spin    { to { transform:rotate(360deg); } }
        @keyframes slideIn { from { transform:translateX(100%); } to { transform:translateX(0); } }
        textarea::placeholder { color: #6b7280; }
      `}</style>

      <div style={{ height: "100vh", background: theme.background, display: "flex", flexDirection: "column", color: theme.text, fontFamily: "'IBM Plex Sans', sans-serif" }}>

        {/* ── HEADER ── */}
        <div style={{ padding: "12px 20px", borderBottom: "1px solid #1a1a1a", display: "flex", alignItems: "center", gap: 10, flexShrink: 0 }}>
          <div style={{ width: 8, height: 8, borderRadius: "50%", background: "#c8a96e", boxShadow: "0 0 6px #c8a96e88" }} />
          <span style={{ fontFamily: "'IBM Plex Mono', monospace", fontSize: 11, color: "#555", letterSpacing: "0.18em" }}>ASSISTANT</span>
          <span style={{ fontSize: 9, color: "#2a2a2a", letterSpacing: "0.1em", fontFamily: "'IBM Plex Mono', monospace" }}>// QWEN 2.5:3b</span>
          <div style={{ flex: 1 }} />
          <button
  onClick={() => setDarkMode(!darkMode)}
  style={{
    background: "transparent",
    border: `1px solid ${theme.border}`,
    borderRadius: "6px",
    padding: "6px 10px",
    cursor: "pointer",
    color: theme.text,
    marginRight: "10px",
  }}
>
  {darkMode ? "☀️" : "🌙"}
</button>
          {/* File count badge */}
          {hasFiles && (
            <div style={{
              display: "flex", alignItems: "center", gap: 5,
              background: "#0d0d1a", border: "1px solid #2a2a4a",
              borderRadius: 5, padding: "3px 8px",
            }}>
              <svg width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="#7b8cde" strokeWidth="2.5" strokeLinecap="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
              </svg>
              <span style={{ fontSize: 9, color: "#7b8cde", fontFamily: "'IBM Plex Mono', monospace" }}>
                {uploadedFiles.length} FILE{uploadedFiles.length !== 1 ? "S" : ""}
              </span>
            </div>
          )}
          <div style={{ display: "flex", alignItems: "center", gap: 5 }}>
            <div style={{ width: 6, height: 6, borderRadius: "50%", background: "#22c55e" }} />
            <span style={{ fontSize: 9, color: "#374151", fontFamily: "'IBM Plex Mono', monospace" }}>{BACKEND_URL}</span>
          </div>
          {messages.length > 0 && (
            <button onClick={clearChat} style={{ background: "transparent", border: "1px solid #222", borderRadius: 5, padding: "4px 10px", fontSize: 10, color: "#444", cursor: "pointer", fontFamily: "'IBM Plex Mono', monospace", letterSpacing: "0.1em", marginLeft: 10 }}>
              CLEAR
            </button>
          )}
        </div>

        {/* ── MESSAGES ── */}
        <div style={{ flex: 1, overflowY: "auto", padding: "24px 20px 8px" }}>
          {isEmpty ? (
            <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", height: "100%", gap: 32, paddingBottom: 40 }}>
              <div style={{ textAlign: "center" }}>
                <div style={{ width: 48, height: 48, borderRadius: "50%", border: `1px solid ${theme.border}`, background: darkMode ? "#141414" : "#ffffff", display: "flex", alignItems: "center", justifyContent: "center", margin: "0 auto 14px", fontSize: 20 }}><span style={{ color: darkMode ? "#ffffff" : "#000000" }}>
  ✦
</span></div>
                <div style={{ fontFamily: "'IBM Plex Mono', monospace", fontSize: 10, color: darkMode ? "#3a3a3a" : "#111111", letterSpacing: "0.2em" }}>HOW CAN I HELP YOU TODAY?</div>
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, width: "100%", maxWidth: 460 }}>
                {SUGGESTIONS.map((s, i) => (
                  <button key={i} onClick={() => handleSend(s)}
                    style={{ background: theme.card, border: `1px solid ${theme.border}`, borderRadius: 8, padding: "10px 12px", textAlign: "left", cursor: "pointer", color: "#555", fontSize: 11.5, lineHeight: 1.5, fontFamily: "'IBM Plex Sans', sans-serif" }}
                    onMouseEnter={(e) => { e.currentTarget.style.borderColor = "#2a2a2a"; e.currentTarget.style.color = "#888"; }}
                    onMouseLeave={(e) => { e.currentTarget.style.borderColor = "#1e1e1e"; e.currentTarget.style.color = "#555"; }}>
                    {s}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div style={{ maxWidth: 700, margin: "0 auto" }}>
              {messages.map((msg) =>
                msg.streaming && msg.content === "" ? (
                  <div key={msg.id} style={{ display: "flex", alignItems: "flex-start", gap: 10, marginBottom: 20 }}>
                    <div style={{ width: 30, height: 30, borderRadius: "50%", background: "#1a1a1a", border: "1px solid #2a2a2a", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 12, fontFamily: "'IBM Plex Mono', monospace", color: "#c8a96e", fontWeight: 600, flexShrink: 0 }}>✦</div>
                    <div style={{ background: "#141414", border: "1px solid #222", borderRadius: "4px 16px 16px 16px", padding: "11px 15px" }}>
                      <TypingDots />
                    </div>
                  </div>
                ) : (
                  <MessageBubble key={msg.id} msg={msg}
                    onShowChunks={(chunks) => setChunkPanel({ open: true, chunks })}
                    theme={theme} />
                )
              )}
              <div ref={bottomRef} />
            </div>
          )}
        </div>

        {/* ── INPUT BAR ── */}
        <div style={{ padding: "12px 20px 16px", borderTop: "1px solid #1a1a1a", flexShrink: 0 }}>
          <div style={{ maxWidth: 700, margin: "0 auto" }}>

            {/* Upload area (collapsible) */}
            {showUpload && (
              <FileUploadArea
                uploadedFiles={uploadedFiles}
                onUpload={(files) => setUploadedFiles((prev) => [...prev, ...files])}
                onRemove={(i) => setUploadedFiles((prev) => prev.filter((_, idx) => idx !== i))}
                theme={theme}
              />
            )}

            {/* Text input row */}
            <div style={{ display: "flex", gap: 8, alignItems: "flex-end", background: theme.card, border: `1px solid ${theme.border}`, borderRadius: 12, padding: "8px 8px 8px 14px" }}
              onFocusCapture={(e) => (e.currentTarget.style.borderColor = "#333")}
              onBlurCapture={(e) => (e.currentTarget.style.borderColor = "#222")}>

              {/* Upload toggle button */}
              <button
                onClick={() => setShowUpload((v) => !v)}
                title="Attach documents"
                style={{
                  width: 30, height: 30, borderRadius: 7, border: "none", flexShrink: 0,
                  background: showUpload || hasFiles ? "#1a1a2e" : "transparent",
                  cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center",
                  transition: "background 0.15s",
                  position: "relative",
                }}
                onMouseEnter={(e) => { if (!showUpload && !hasFiles) e.currentTarget.style.background = "#151515"; }}
                onMouseLeave={(e) => { if (!showUpload && !hasFiles) e.currentTarget.style.background = "transparent"; }}
              >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
                  stroke={showUpload || hasFiles ? "#7b8cde" : "#444"} strokeWidth="2" strokeLinecap="round">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                  <polyline points="17 8 12 3 7 8"/>
                  <line x1="12" y1="3" x2="12" y2="15"/>
                </svg>
                {hasFiles && (
                  <span style={{
                    position: "absolute", top: 2, right: 2, width: 8, height: 8,
                    borderRadius: "50%", background: "#c8a96e", fontSize: 6,
                    display: "flex", alignItems: "center", justifyContent: "center",
                    color: "#0d0d0d", fontFamily: "'IBM Plex Mono', monospace", fontWeight: 700,
                  }}>{uploadedFiles.length}</span>
                )}
              </button>

              <textarea ref={taRef} value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={handleKey}
                placeholder="Ask me anything... (Enter to send, Shift+Enter for new line)"
                rows={1}
                style={{ flex: 1, background: "transparent", border: "none", outline: "none", color: theme.text, fontSize: 13.5, lineHeight: 1.6, fontWeight: 300, resize: "none", maxHeight: 120, overflowY: "auto", paddingTop: 2, fontFamily: "'IBM Plex Sans', sans-serif" }}
                onInput={(e) => { e.target.style.height = "auto"; e.target.style.height = Math.min(e.target.scrollHeight, 120) + "px"; }}
              />
              <button onClick={() => handleSend()} disabled={!input.trim() || loading}
                style={{ width: 34, height: 34, borderRadius: 8, border: "none", background: input.trim() && !loading ? "#c8a96e" : "#1e1e1e", cursor: input.trim() && !loading ? "pointer" : "not-allowed", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0, transition: "background 0.15s" }}>
                {loading
                  ? <div style={{ width: 14, height: 14, border: "2px solid #333", borderTop: "2px solid #888", borderRadius: "50%", animation: "spin 0.8s linear infinite" }} />
                  : <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#ffffff" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/></svg>
                }
              </button>
            </div>
            <div style={{ maxWidth: 700, margin: "6px auto 0", textAlign: "center", fontSize: 9.5, color: darkMode ? "#2a2a2a" : "#6b7280", fontFamily: "'IBM Plex Mono', monospace", letterSpacing: "0.08em" }}>
              SHIFT+ENTER FOR NEW LINE · POWERED BY QWEN  VIA OLLAMA
            </div>
          </div>
        </div>
      </div>

      {/* ── CHUNK SIDE PANEL ── */}
      <ChunkPanel
        chunks={chunkPanel.chunks}
        isOpen={chunkPanel.open}
        onClose={() => setChunkPanel({ open: false, chunks: [] })}
        theme={theme}
      />
    </>
  );
}