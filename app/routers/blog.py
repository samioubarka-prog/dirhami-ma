from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.models import BlogArticle
from app.schemas.schemas import BlogArticleResponse

router = APIRouter(prefix="/blog", tags=["blog"])

@router.get("/", response_model=List[BlogArticleResponse])
def get_articles(
    categorie: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    query = db.query(BlogArticle).filter(BlogArticle.published == True)
    if categorie:
        query = query.filter(BlogArticle.categorie == categorie)
    return query.offset(skip).limit(limit).all()

@router.get("/{slug}", response_model=BlogArticleResponse)
def get_article(slug: str, db: Session = Depends(get_db)):
    article = db.query(BlogArticle).filter(BlogArticle.slug == slug, BlogArticle.published == True).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return article

@router.get("/categories/list")
def get_categories(db: Session = Depends(get_db)):
    cats = db.query(BlogArticle.categorie).distinct().all()
    return [c[0] for c in cats if c[0]]
