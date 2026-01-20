import React, { useState } from "react";

function App() {
  const [resume, setResume] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!resume || !jobDescription) {
      alert("Please upload a resume and enter a job description");
      return;
    }

    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("job_description", jobDescription);

    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      alert("Error connecting to backend");
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial, sans-serif" }}>
      <h1>AI Resume Analyzer</h1>

      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setResume(e.target.files[0])}
      />

      <br /><br />

      <textarea
        rows="6"
        cols="70"
        placeholder="Paste job description here..."
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
      />

      <br /><br />

      <button onClick={handleSubmit}>
        {loading ? "Analyzing..." : "Analyze Resume"}
      </button>

      {result && (
        <div style={{ marginTop: "30px" }}>
          <h2>Results</h2>

          <p><b>Keyword Match:</b> {result.keyword_match_score}%</p>
          <p><b>Semantic Match:</b> {result.semantic_match_score}%</p>

          <p>
            <b>Missing Skills:</b>{" "}
            {result.missing_skills.length > 0
              ? result.missing_skills.join(", ")
              : "None"}
          </p>

          <h3>Suggestions</h3>
          <ul>
            {result.suggestions.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
