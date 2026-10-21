import sqlite3
import os

DB_PATH = "users.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def init_user_db():
    """Initializes users table and ensures necessary columns and default admin exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        email TEXT,
        role TEXT DEFAULT 'Faculty',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    
    # Check if existing table has email and role columns
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if "email" not in columns:
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN email TEXT")
        except Exception:
            pass
            
    if "role" not in columns:
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'Faculty'")
        except Exception:
            pass
            
    if "created_at" not in columns:
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        except Exception:
            pass
            
    conn.commit()
    
    # Check if admin user exists; if not, create default
    cursor.execute("SELECT username, password FROM users WHERE LOWER(username) = 'admin'")
    admin_row = cursor.fetchone()
    if not admin_row:
        cursor.execute(
            "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
            ("admin", "1234", "admin@uit.edu", "Administrator")
        )
        conn.commit()
    
    conn.close()

def authenticate_user(username_or_email, password):
    """Verifies credentials against users.db."""
    u_input = (username_or_email or "").strip()
    p_input = (password or "").strip()
    
    if not u_input:
        return False, "Please enter your username or email.", None
    if not p_input:
        return False, "Please enter your password.", None
        
    init_user_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT username, password, email, role 
        FROM users 
        WHERE LOWER(username) = LOWER(?) OR LOWER(email) = LOWER(?)
    """, (u_input, u_input))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return False, f"User '{u_input}' not found. Please check spelling or create an account via Sign Up.", None
        
    stored_password = row["password"]
    if stored_password != p_input:
        return False, "Incorrect password. Please try again or use Forgot Password.", None
        
    user_data = {
        "username": row["username"],
        "email": row["email"] or "",
        "role": row["role"] or "Faculty"
    }
    return True, f"Welcome back, {row['username']}!", user_data

def register_user(username, password, email="", role="Faculty"):
    """Registers a new user in users.db."""
    uname = (username or "").strip()
    pwd = (password or "").strip()
    mail = (email or "").strip()
    user_role = (role or "Faculty").strip()
    
    if not uname:
        return False, "Username is required."
    if len(uname) < 3:
        return False, "Username must be at least 3 characters long."
    if " " in uname:
        return False, "Username cannot contain spaces."
    if not pwd or len(pwd) < 4:
        return False, "Password must be at least 4 characters long."
        
    init_user_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check username collision
    cursor.execute("SELECT username FROM users WHERE LOWER(username) = LOWER(?)", (uname,))
    if cursor.fetchone():
        conn.close()
        return False, f"Username '{uname}' is already taken. Please choose another username."
        
    # Check email collision if email provided
    if mail:
        cursor.execute("SELECT username FROM users WHERE LOWER(email) = LOWER(?)", (mail,))
        if cursor.fetchone():
            conn.close()
            return False, f"Email '{mail}' is already registered with another account. Please sign in."
            
    try:
        cursor.execute(
            "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
            (uname, pwd, mail, user_role)
        )
        conn.commit()
        conn.close()
        return True, f"Account '{uname}' created successfully! You are now signed in."
    except Exception as e:
        conn.close()
        return False, f"Registration failed: {str(e)}"

def reset_password(username_or_email, new_password):
    """Resets password for an existing user."""
    u_input = (username_or_email or "").strip()
    new_pwd = (new_password or "").strip()
    
    if not u_input:
        return False, "Please enter your username or email."
    if not new_pwd or len(new_pwd) < 4:
        return False, "New password must be at least 4 characters long."
        
    init_user_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT username FROM users 
        WHERE LOWER(username) = LOWER(?) OR LOWER(email) = LOWER(?)
    """, (u_input, u_input))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return False, f"No user account found matching '{u_input}'."
        
    target_username = row["username"]
    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_pwd, target_username))
    conn.commit()
    conn.close()
    return True, f"Password for '{target_username}' has been successfully reset! Please sign in with your new password."
