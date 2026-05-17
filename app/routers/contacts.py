from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ContactMessage
from app.schemas import ContactCreate

router = APIRouter()

@router.post("/")
async def send_message(data: ContactCreate, db: Session = Depends(get_db)):
    msg = ContactMessage(**data.dict())
    db.add(msg)
    db.commit()
    return {"message": "Message envoye avec succes", "id": msg.id}
