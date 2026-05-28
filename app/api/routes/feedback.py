from fastapi import APIRouter
from app.schemas.models import FeedbackRequest

router = APIRouter(tags=["feedback"])

@router.post("/feedback")
def feedback(req: FeedbackRequest):
    return {"received": True, "query_id": req.query_id, "label": req.label, "notes": req.notes}