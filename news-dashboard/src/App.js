import React, { useEffect, useState } from "react";
import axios from "axios";

const apiUrl = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000"; // Fallback to local API if environment variable is missing

function App() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(false);

  // Fetch articles from FastAPI
  useEffect(() => {
    axios.get(`${apiUrl}/articles/`)
      .then(response => {
        if (response.data && Array.isArray(response.data.articles)) {
          setArticles(response.data.articles);
        } else {
          console.error("Unexpected API response structure:", response.data);
          setArticles([]);
        }
      })
      .catch(error => {
        console.error("Error fetching articles:", error);
      });
  }, []);

  // Handle rewriting an article
  const handleRewrite = async (id) => {
    console.log(`🔹 Rewrite button clicked for article ID: ${id}`); // Debug log
  
    const article = articles.find(article => article.id === id);
    if (!article) {
      console.error("❌ Article not found.");
      return;
    }
  
    try {
      const response = await axios.post(`${apiUrl}/articles/select/${id}`);
      console.log("✅ API Response:", response.data); // Debug log
  
      if (response.data && response.data.message) {
        setArticles(prevArticles => prevArticles.map(article => 
          article.id === id ? { ...article, rewrite_status: "pending" } : article
        ));
      }
    } catch (error) {
      console.error("❌ Error selecting article for rewrite:", error);
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h2>News Articles</h2>
      <ul>
        {articles.map((article) => (
          <li key={article.id} style={{ marginBottom: "10px" }}>
            <strong>{article.title}</strong>
            <button 
              style={{ marginLeft: "10px", cursor: "pointer" }}
              onClick={() => handleRewrite(article.id)}
              disabled={article.rewrite_status !== "not_selected"}
            >
              {article.rewrite_status === "pending" ? "Rewriting..." : 
               article.rewrite_status === "completed" ? "Rewritten" : "Rewrite"}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;