import os
import jwt
import datetime
from fastapi import APIRouter, HTTPException, Depends
from models import LoginRequest, SignupRequest, GoogleAuthRequest, LoginResponse
import database
from google.oauth2 import id_token
from google.auth.transport import requests

router = APIRouter()

SECRET_KEY = os.environ.get("JWT_SECRET", "ammachi-secret-key-12345")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")

def create_token(username: str):
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@router.get("/auth/config")
def get_auth_config():
    return {"google_client_id": GOOGLE_CLIENT_ID}

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    user = database.get_user(request.username)
    if user and database.verify_password(request.password, user['password_hash']):
        token = create_token(user['username'])
        return LoginResponse(
            success=True, 
            message="Welcome back, Kanna!", 
            token=token,
            username=user['username']
        )
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/signup", response_model=LoginResponse)
def signup(request: SignupRequest):
    if not request.username or not request.password:
        raise HTTPException(status_code=400, detail="Username and password required")
    
    success = database.create_user(request.username, password=request.password)
    if success:
        token = create_token(request.username)
        return LoginResponse(
            success=True,
            message="Account created! Welcome to Ammachi's class.",
            token=token,
            username=request.username
        )
    else:
        raise HTTPException(status_code=400, detail="Username already exists")

from google_auth_oauthlib.flow import Flow
from fastapi import Form

GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:8501") # Default port for Streamlit

# Set up the OAuth2 flow
client_config = {
    "web": {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": [GOOGLE_REDIRECT_URI],
    }
}

@router.get("/auth/google/url")
def get_google_auth_url():
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        raise HTTPException(status_code=500, detail="Google OAuth not configured in .env")
    flow = Flow.from_client_config(client_config, scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'])
    flow.redirect_uri = GOOGLE_REDIRECT_URI
    authorization_url, state = flow.authorization_url(prompt='consent')
    return {"url": authorization_url}

@router.post("/auth/google/exchange", response_model=LoginResponse)
def google_exchange(code: str = Form(...)):
    try:
        flow = Flow.from_client_config(client_config, scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'])
        flow.redirect_uri = GOOGLE_REDIRECT_URI
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        # Timeout handling is implicit in sync call
        idinfo = id_token.verify_oauth2_token(credentials.id_token, requests.Request(), GOOGLE_CLIENT_ID)
        google_id = idinfo['sub']
        email = idinfo.get('email')
        name = idinfo.get('name', email.split('@')[0] if email else 'student')
        
        user = database.get_user_by_google_id(google_id)
        if not user:
            username = email if email else f"user_{google_id[:8]}"
            # Prevent unique constraint crash
            existing = database.get_user(username)
            if existing: username = f"{username}_{google_id[:4]}"
            
            database.create_user(username, google_id=google_id)
            user = database.get_user(username)
        
        token = create_token(user['username'])
        return LoginResponse(success=True, message=f"Namaste {name}!", token=token, username=user['username'])
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=401, detail=f"Google Exchange failed: {str(e)}")

@router.post("/auth/google", response_model=LoginResponse)
def google_auth(request: GoogleAuthRequest):
    # This remains for optional ID token login from clients
    try:
        idinfo = id_token.verify_oauth2_token(request.id_token, requests.Request(), GOOGLE_CLIENT_ID)
        google_id = idinfo['sub']
        email = idinfo.get('email')
        name = idinfo.get('name', email.split('@')[0] if email else 'student')
        
        user = database.get_user_by_google_id(google_id)
        if not user:
            username = email if email else f"user_{google_id[:8]}"
            database.create_user(username, google_id=google_id)
            user = database.get_user(username)
        
        token = create_token(user['username'])
        return LoginResponse(success=True, message=f"Namaste {name}!", token=token, username=user['username'])
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Google Auth failed: {str(e)}")
