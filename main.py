from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Article

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from React frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def read_root():
    return {"message": "FastAPI is running successfully!"}

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/articles/")
def get_articles(db: Session = Depends(get_db)):
    articles = db.query(Article).all()
    return {"articles": [{"id": article.id, "title": article.title, "rewrite_status": article.rewrite_status} for article in articles]}

@app.get("/articles/{article_id}")
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        return {"error": "Article not found"}
    
    return {"id": article.id, "title": article.title, "rewrite_status": article.rewrite_status}

@app.post("/articles/select/{article_id}")
def select_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        return {"error": "Article not found"}
    
    article.rewrite_status = "selected_for_rewriting"  # Update status to 'selected_for_rewriting'
    db.commit()
    return {"message": f"✅ Article {article_id} selected for rewriting"}

@app.post("/articles/rewrite/{article_id}")
def rewrite_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        return {"error": "Article not found"}
    
    article.rewrite_status = "rewritten"  # Update status to 'rewritten'
    db.commit()
    return {"message": f"✅ Article {article_id} marked as rewritten"}