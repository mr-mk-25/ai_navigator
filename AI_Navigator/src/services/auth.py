import json
import os
from datetime import datetime
import hashlib

# Users data file path
def get_users_file():
    # Navigate from src/services/auth.py up two directories to C:\AI_Navigator\
    current_dir = os.path.dirname(os.path.abspath(__file__))  # src/services
    services_dir = os.path.dirname(current_dir)  # src
    project_dir = os.path.dirname(services_dir)  # C:\AI_Navigator
    return os.path.join(project_dir, "data", "users.json")

def load_users():
    """Load users from JSON file."""
    users_file = get_users_file()
    if os.path.exists(users_file):
        with open(users_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to JSON file."""
    users_file = get_users_file()
    with open(users_file, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

def hash_password(password):
    """Hash password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def user_exists(username):
    """Check if user exists."""
    users = load_users()
    return username in users

def signup_user(username, email, password, full_name=""):
    """Create a new user account."""
    users = load_users()
    
    if username in users:
        return False, "Username already exists!"
    
    if any(user["email"] == email for user in users.values()):
        return False, "Email already registered!"
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters!"
    
    users[username] = {
        "email": email,
        "password": hash_password(password),
        "full_name": full_name,
        "created_at": datetime.now().isoformat(),
        "profile": {
            "skills": [],
            "preferred_duration": "3 months",
            "interests": []
        }
    }
    
    save_users(users)
    return True, "Account created successfully!"

def login_user(username, password):
    """Authenticate user login."""
    users = load_users()
    
    if username not in users:
        return False, "Username not found!"
    
    user = users[username]
    if user["password"] != hash_password(password):
        return False, "Incorrect password!"
    
    return True, user

def get_user_profile(username):
    """Get user profile data."""
    users = load_users()
    if username in users:
        return users[username]
    return None

def update_user_profile(username, profile_data):
    """Update user profile."""
    users = load_users()
    if username in users:
        users[username]["profile"] = profile_data
        save_users(users)
        return True
    return False
