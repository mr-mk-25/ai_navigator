# Authentication System Architecture

## System Overview

The AI Internship Navigator includes a complete authentication and user management system that provides secure user accounts, profile customization, and persistent data storage.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    STREAMLIT APPLICATION                     │
│                         (app.py)                              │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │            AUTHENTICATION LAYER                      │    │
│  ├─────────────────────────────────────────────────────┤    │
│  │  • Login/Signup Pages                               │    │
│  │  • Session State Management                         │    │
│  │  • User Route Protection                            │    │
│  └─────────────────────────────────────────────────────┘    │
│            ↓                            ↓                    │
│  ┌──────────────────────┐  ┌──────────────────────────┐    │
│  │ AUTH SERVICE MODULE  │  │ MAIN DASHBOARD           │    │
│  │  (services/auth.py)  │  │ (Profile Settings, etc.) │    │
│  ├──────────────────────┤  └──────────────────────────┘    │
│  │ • signup_user()      │                                   │
│  │ • login_user()       │                                   │
│  │ • get_user_profile() │                                   │
│  │ • update_profile()   │                                   │
│  │ • password hashing   │                                   │
│  └──────────────────────┘                                   │
│            ↓                                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │          DATA STORAGE LAYER                          │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │ • data/users.json (User credentials & profiles)     │  │
│  │ • JSON file operations (load/save)                  │  │
│  │ • File path resolution                              │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Authentication Layer (app.py)

**Purpose**: Handle user authentication flow and UI

**Key Responsibilities**:
- Display login/signup interface
- Manage authentication state via `st.session_state`
- Control access to main dashboard
- Render profile settings interface

**Authentication State Variables**:
```python
st.session_state.authenticated  # Boolean: True if user is logged in
st.session_state.username       # String: Current user's username
```

**Flow**:
1. Check `authenticated` state on page load
2. If False → Show login/signup page
3. If True → Show dashboard and recommendations

### 2. Auth Service Module (services/auth.py)

**Purpose**: Handle all authentication logic and user data operations

**Key Functions**:

#### `signup_user(username, email, password, full_name="")`
Creates a new user account with validation.

**Validations**:
- Username uniqueness
- Email uniqueness
- Password minimum length (6 characters)
- Returns tuple: (success: bool, message: str)

**Data Structure Created**:
```json
{
  "username": {
    "email": "user@example.com",
    "password": "<SHA256_HASH>",
    "full_name": "User Name",
    "created_at": "2025-12-27T10:30:45.123456",
    "profile": {
      "skills": ["Python", "Data Analysis"],
      "preferred_duration": "3 months",
      "interests": ["AI", "Data Science"]
    }
  }
}
```

#### `login_user(username, password)`
Authenticates user credentials.

**Process**:
1. Load users from JSON
2. Check if username exists
3. Hash provided password
4. Compare with stored hash
5. Return user data if successful

#### `get_user_profile(username)`
Retrieves user profile data.

**Returns**: Full user object or None

#### `update_user_profile(username, profile_data)`
Updates user profile settings.

**Updates**: skills, preferred_duration, interests

### 3. Data Storage Layer (data/users.json)

**Format**: JSON file with user accounts

**Structure**:
```json
{
  "username1": {
    "email": "...",
    "password": "...",
    "full_name": "...",
    "created_at": "...",
    "profile": {...}
  },
  "username2": {...}
}
```

**File Operations**:
- `load_users()`: Read from JSON
- `save_users(dict)`: Write to JSON
- Automatic file creation if missing

## Security Implementation

### Password Security

**Method**: SHA-256 Hashing

```python
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
```

**Process**:
1. User enters password
2. Password hashed using SHA-256
3. Hash stored in users.json
4. Original password never saved

**Validation**:
```python
stored_hash == hash(provided_password)  # True = valid
```

### Data Protection

1. **Sensitive Data**:
   - Passwords hashed immediately
   - Plain text passwords never logged
   - User data isolated per account

2. **Session Management**:
   - Streamlit session state for authentication
   - Separate session per browser/tab
   - Logout clears all session data

3. **File Access Control**:
   - users.json stored locally
   - File permissions managed by OS
   - Path resolution prevents directory traversal

## User Flow Diagrams

### Sign Up Flow

```
User Input
    ↓
[Validate Input]
    ↓
[Check Uniqueness]
    ├─ Yes → Create Account
    │         ↓
    │     [Hash Password]
    │         ↓
    │     [Save to JSON]
    │         ↓
    │     Success Message
    │
    └─ No → Error Message
```

### Login Flow

```
User Input (username, password)
    ↓
[Load Users from JSON]
    ↓
[Check Username Exists]
    ├─ No → Username not found error
    │
    └─ Yes → [Hash Password]
              ↓
          [Compare with Stored Hash]
              ├─ Match → Set session state
              │          ↓
              │      Redirect to Dashboard
              │
              └─ No Match → Password error
```

### Dashboard Access Flow

```
Page Load
    ↓
[Check st.session_state.authenticated]
    ├─ False → Show Login/Signup
    │
    └─ True → [Load User Profile]
               ↓
           Show Dashboard
               ↓
           Display Settings Tab
```

## Integration with Main Features

### Profile Settings Integration

1. User logs in → `st.session_state.username` set
2. Profile Settings tab loads user data via `get_user_profile(username)`
3. User edits and saves → `update_user_profile(username, data)`
4. Recommendations use updated profile data

### Dashboard Integration

1. Authenticated users can:
   - Select existing student profiles
   - Create custom profiles
   - Get AI-powered recommendations
   - Filter opportunities

2. Profile data flows to:
   - Scoring algorithm (skill matching)
   - Recommendation engine
   - Statistics display

## Error Handling

| Error | Status | Message | Action |
|-------|--------|---------|--------|
| Username exists | signup | "Username already exists!" | Suggest new username |
| Email exists | signup | "Email already registered!" | Suggest login |
| Short password | signup | "Password must be 6+ chars!" | Request longer password |
| Username not found | login | "Username not found!" | Offer signup |
| Wrong password | login | "Incorrect password!" | Suggest password reset |

## File Paths

```
C:\AI_Navigator\
├── src/
│   ├── app.py                    # Main app with auth flow
│   └── services/
│       └── auth.py               # Auth service module
├── data/
│   ├── users.json                # User credentials
│   ├── students.json             # Sample profiles
│   └── opportunities.json        # Opportunities data
└── [this file]
```

## Configuration

### Default Settings

```python
# Password validation
MIN_PASSWORD_LENGTH = 6

# Hash algorithm
ALGORITHM = "SHA-256"

# Session management
SESSION_TIMEOUT = None  # Session persists
```

### Customization Options

To modify authentication behavior, edit `services/auth.py`:

```python
# Change password requirements
if len(password) < 8:  # Increase from 6 to 8

# Add email validation
if not validate_email(email):

# Add username format rules
if not username.isalnum():
```

## Database Migration (Future)

To scale from JSON to database:

1. **Create database schema**:
   - Users table
   - Profiles table
   - Sessions table

2. **Replace file operations**:
   - `load_users()` → Database query
   - `save_users()` → Database insert/update
   - `get_user_profile()` → Database join

3. **Update imports**:
   - Replace JSON operations with ORM calls
   - Use SQLAlchemy or similar

4. **Example migration**:
   ```python
   # Before
   users = load_users()  # From JSON
   
   # After
   users = db.session.query(User).all()  # From database
   ```

## Security Recommendations for Production

1. **Upgrade Password Hashing**
   - Use bcrypt or argon2 instead of SHA-256
   - Add salt to password hashing
   - Implement key derivation functions

2. **Add Email Verification**
   - Send verification email on signup
   - Prevent account access until verified

3. **Implement Password Recovery**
   - Send reset token via email
   - Time-limited reset links

4. **Add Rate Limiting**
   - Limit login attempts
   - Prevent brute force attacks

5. **Use HTTPS**
   - Encrypt all communication
   - Use SSL certificates

6. **Implement JWT Tokens**
   - Token-based authentication
   - Stateless sessions

7. **Database**
   - Move from JSON to secure database
   - Implement connection encryption
   - Regular backups

## Testing

### Manual Testing Checklist

- [ ] Sign up with valid credentials
- [ ] Sign up with existing username (error)
- [ ] Sign up with invalid email (error)
- [ ] Sign up with short password (error)
- [ ] Login with correct credentials
- [ ] Login with wrong password (error)
- [ ] Login with non-existent username (error)
- [ ] Update profile settings
- [ ] Verify profile persists after logout/login
- [ ] Switch between users
- [ ] Logout functionality

---

**Version**: 1.0.0  
**Last Updated**: December 27, 2025  
**Status**: Production Ready (with recommendations for scaling)
