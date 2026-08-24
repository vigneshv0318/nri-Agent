from datetime import datetime

try:
    from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
    from sqlalchemy.orm import relationship
    from database.connection import Base

    if Base is not None:
        class User(Base):
            __tablename__ = "users"

            id = Column(Integer, primary_key=True, index=True)
            username = Column(String(100), unique=True, index=True, nullable=False)
            password_hash = Column(String(255), nullable=True)
            google_id = Column(String(255), unique=True, index=True, nullable=True)
            points = Column(Integer, default=0)
            current_language = Column(String(50), default="Tamil")
            created_at = Column(DateTime, default=datetime.utcnow)
            updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

            # Relationships
            progress_records = relationship("LearningProgress", back_populates="user", cascade="all, delete-orphan")
            stamps = relationship("CulturalStamp", back_populates="user", cascade="all, delete-orphan")
            sessions = relationship("LearningSession", back_populates="user", cascade="all, delete-orphan")

        class LearningProgress(Base):
            __tablename__ = "learning_progress"

            id = Column(Integer, primary_key=True, index=True)
            user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
            module = Column(String(50), nullable=False)  # 'writing', 'voice', 'culture'
            activity = Column(String(150), nullable=False)  # e.g., 'Letter அ Tracing', 'Pongal Quiz'
            score = Column(Integer, default=0)
            language = Column(String(50), default="Tamil")
            created_at = Column(DateTime, default=datetime.utcnow)

            user = relationship("User", back_populates="progress_records")

        class CulturalStamp(Base):
            __tablename__ = "cultural_stamps"

            id = Column(Integer, primary_key=True, index=True)
            user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
            stamp_name = Column(String(100), nullable=False)
            badge_icon = Column(String(100), default="🪔")
            earned_at = Column(DateTime, default=datetime.utcnow)

            user = relationship("User", back_populates="stamps")

        class LearningSession(Base):
            __tablename__ = "learning_sessions"

            id = Column(Integer, primary_key=True, index=True)
            user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
            module = Column(String(50), nullable=False)
            score = Column(Integer, default=0)
            session_metadata = Column(JSON, nullable=True)
            created_at = Column(DateTime, default=datetime.utcnow)

            user = relationship("User", back_populates="sessions")
    else:
        User = None
        LearningProgress = None
        CulturalStamp = None
        LearningSession = None

except Exception:
    User = None
    LearningProgress = None
    CulturalStamp = None
    LearningSession = None
