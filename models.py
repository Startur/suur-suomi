from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from database import Base
from datetime import datetime

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    source_url = Column(String, unique=True, nullable=False)
    source = Column(String, nullable=False)
    author = Column(String, nullable=True)
    published_at = Column(DateTime, nullable=True)
    rewrite_status = Column(String, default='not_selected')
    created_at = Column(DateTime, default=datetime.utcnow)
    selected_for_rewrite = Column(Boolean, default=False)