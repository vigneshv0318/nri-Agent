import sqlite3
import json
from passlib.context import CryptContext

DB_NAME = "ammachi.db"
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Update table to include password_hash and google_id for OAuth
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, 
                  password_hash TEXT, 
                  google_id TEXT,
                  points INTEGER DEFAULT 0, 
                  stamps TEXT DEFAULT '[]')''')
    
    # Check if we need to add columns to existing table (migration)
    c.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in c.fetchall()]
    if "password_hash" not in columns:
        c.execute("ALTER TABLE users ADD COLUMN password_hash TEXT")
    conn.commit()
    
    # Bootstrap default student user if not exists
    c.execute("SELECT username FROM users WHERE username='student'")
    if not c.fetchone():
        hashed_pwd = pwd_context.hash("password123")
        c.execute("INSERT INTO users (username, password_hash, points, stamps) VALUES (?, ?, ?, ?)",
                  ('student', hashed_pwd, 0, json.dumps([])))
        conn.commit()
        
    conn.close()

def get_user(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT username, points, stamps, password_hash, google_id FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    if user:
        return {
            "username": user[0], 
            "points": user[1], 
            "stamps": json.loads(user[2]),
            "password_hash": user[3],
            "google_id": user[4]
        }
    return None

def create_user(username, password=None, google_id=None):
    hashed_pwd = pwd_context.hash(password) if password else None
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password_hash, google_id, points, stamps) VALUES (?, ?, ?, ?, ?)", 
                  (username, hashed_pwd, google_id, 0, json.dumps([])))
        conn.commit()
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()
    return True

def verify_password(plain_password, hashed_password):
    if not hashed_password: return False
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_google_id(google_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT username, points, stamps, password_hash, google_id FROM users WHERE google_id=?", (google_id,))
    user = c.fetchone()
    conn.close()
    if user:
        return {
            "username": user[0], 
            "points": user[1], 
            "stamps": json.loads(user[2]),
            "password_hash": user[3],
            "google_id": user[4]
        }
    return None

def update_score(username, points_add, new_stamp=None):
    user = get_user(username)
    if not user: return None
    new_points = user['points'] + points_add
    stamps = user['stamps']
    
    if new_stamp and new_stamp not in stamps:
        stamps.append(new_stamp)
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE users SET points=?, stamps=? WHERE username=?", (new_points, json.dumps(stamps), username))
    conn.commit()
    conn.close()
    return {"points": new_points, "stamps": stamps}
