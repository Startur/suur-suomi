import React, { useEffect, useState } from "react";
import axios from "axios";

const apiUrl = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000"; // Fallback to local API if environment variable is missing

function App() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(false);  // Track loading state
  const [progress, setProgress] = useState(0);  // Track progress of rewriting

  // Fetch articles from FastAPI
  useEffect(() => {
    axios.get(`${apiUrl}/articles/`)
      .then(response => {
        console.log("API response:", response);  // Log the full API response
        if (response.data && Array.isArray(response.data.articles)) {
          console.log("Articles data:", response.data.articles);
          setArticles(response.data.articles);
        } else {
          console.error("Articles not found or invalid structure:", response.data);
          setArticles([]);
        }
      })
      .catch(error => {
        console.error("Error fetching articles:", error);
      });
  }, []);

  // Check for missing content and update with default content
  useEffect(() => {
    const checkAndUpdateArticles = async () => {
      try {
        const response = await axios.get(`${apiUrl}/articles/`);
        const articlesToUpdate = response.data.articles.filter(article => !article.content);
        
        if (articlesToUpdate.length > 0) {
          await Promise.all(articlesToUpdate.map(article => 
            axios.put(`${apiUrl}/articles/${article.id}`, { content: "This is default content" })
          ));
          console.log("Missing content updated with default content.");
        }
      } catch (error) {
        console.error("Error checking or updating articles:", error);
      }
    };

    checkAndUpdateArticles();
  }, []);

  // Handle rewriting an article
  const handleRewrite = (id) => {
    // Find the article and extract the original content
    const article = articles.find(article => article.id === id);
    const originalContent = article ? article.content : "Content not available";

    console.log("Original Article Content:", originalContent);  // Log the original content

    // Open a new window for displaying the original and rewritten articles
    const newWindow = window.open('', '_blank', 'width=1000,height=600');
    
    // Check if the new window was opened successfully
    if (newWindow) {
      console.log("New window opened successfully!");
    } else {
      console.error("Failed to open new window.");
    }

    // Ensure the window is ready to receive content
    newWindow.document.write(`
      <html>
        <head><title>Article Rewrite</title></head>
        <body>
          <div style="display: flex; justify-content: space-between; padding: 20px;">
            <div style="width: 45%; border-right: 1px solid #ccc;">
              <h3>Original Article</h3>
              <p id="originalContent">${originalContent}</p>  <!-- Original content is inserted here -->
            </div>
            <div style="width: 45%; padding-left: 20px;">
              <h3>Rewritten Article</h3>
              <p id="rewrittenContent">Loading...</p> <!-- Rewritten content placeholder -->
            </div>
          </div>
        </body>
      </html>
    `);

    // Make sure the content is loaded in the window
    newWindow.onload = function() {
      console.log("New window content loaded!");
    };

    // Simulate rewriting progress in the new window
    setLoading(true);
    setProgress(0);

    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev < 100) {
          return prev + 10;  // Increase progress by 10% every 500ms
        } else {
          clearInterval(interval);
          const rewrittenContent = "This is the rewritten content based on the original article.";
          newWindow.document.getElementById('rewrittenContent').textContent = rewrittenContent;  // Display rewritten content
          setLoading(false);
          return 100;
        }
      });
    }, 500);

    // Update the article status (optional)
    axios.post(`${apiUrl}/articles/select/${id}`)
      .then(() => {
        setArticles(prevArticles => 
          prevArticles.map(article => 
            article.id === id ? { ...article, selected_for_rewrite: true, content: "This is the rewritten content" } : article
          )
        );
      })
      .catch(error => {
        console.error("Error selecting article:", error);
      });
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
              disabled={article.selected_for_rewrite || loading}  // Disable if already selected or if loading
            >
              {article.selected_for_rewrite ? "Rewriting..." : "Rewrite"}
            </button>
            {article.selected_for_rewrite && (
              <div style={{ marginTop: "10px", color: "gray" }}>
                <h4>Rewritten Content:</h4>
                <p>{article.content}</p>
              </div>
            )}
            {loading && (
              <div style={{ marginTop: "10px" }}>
                <progress value={progress} max="100" style={{ width: "100%" }} />
                <p>Progress: {progress}%</p>
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;