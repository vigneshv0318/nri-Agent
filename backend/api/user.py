from fastapi import APIRouter, Depends, HTTPException
from database.connection import get_db
from database import crud
from api.auth import get_current_user
from schemas.user import UserProfileResponse, UpdateLanguageRequest

router = APIRouter()

@router.get("/profile", response_model=UserProfileResponse)
def get_user_profile(
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    return crud.get_user_progress_summary(db, current_user)

@router.put("/language")
def update_language(
    request: UpdateLanguageRequest,
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    updated = crud.update_user_language(db, current_user.id, request.language)
    return {"success": True, "language": updated.current_language}

@router.get("/stamps")
def get_stamps(
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    return [
        {
            "id": s.id,
            "stamp_name": s.stamp_name,
            "badge_icon": s.badge_icon,
            "earned_at": s.earned_at.isoformat() if hasattr(s.earned_at, "isoformat") else str(s.earned_at)
        }
        for s in current_user.stamps
    ]
