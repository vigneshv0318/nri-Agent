from database.connection import Base, engine, get_db, init_db, SessionLocal
from database import crud

try:
    from database.models import User, LearningProgress, CulturalStamp, LearningSession
except Exception:
    User = None
    LearningProgress = None
    CulturalStamp = None
    LearningSession = None

__all__ = [
    "Base",
    "engine",
    "get_db",
    "init_db",
    "SessionLocal",
    "User",
    "LearningProgress",
    "CulturalStamp",
    "LearningSession",
    "crud"
]
