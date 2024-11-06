from fastapi import APIRouter, Depends

from app.db.session import DbConnection
from app.utils.dependency import get_db

router = APIRouter()

@router.get("/notes")
def get_notes(db: DbConnection = Depends(get_db)):
    query = "SELECT * FROM notes"
    notes = db.fetch_query(query)
    print(f"Retrieved {len(notes)} notes")
    return {"notes": notes}
