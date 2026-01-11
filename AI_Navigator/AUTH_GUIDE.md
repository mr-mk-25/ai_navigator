# Authentication Guide - AI Internship Navigator

## Overview
The AI Internship Navigator now features a complete user authentication system with login and signup pages. Users can create custom profiles, save their preferences, and get personalized internship recommendations.

## Features

### 1. **User Authentication**
- **Sign Up**: Create a new account with username, email, full name, and password
- **Login**: Secure login with username and password
- **Password Security**: Passwords are hashed using SHA-256 algorithm
- **Session Management**: Secure session handling with Streamlit session state

### 2. **User Profile Management**
- Store user credentials securely
- Save skills, preferred internship duration, and interests
- Edit profile settings anytime
- View account creation date

### 3. **Persistent User Data**
- User credentials stored in `data/users.json`
- User profiles saved with account data
- Automatic profile synchronization

## Getting Started

### Demo Account
To test the application without creating a new account:

**Username**: `demo_user`  
**Password**: `demo123`

### Creating a New Account

1. Click on the **"Sign Up"** tab on the login page
2. Fill in the following information:
   - **Username**: Choose a unique username (minimum 1 character)
   - **Email**: Your email address
   - **Full Name**: Your complete name
   - **Password**: At least 6 characters
   - **Confirm Password**: Re-enter your password

3. Click **"Create Account"**
4. You'll be redirected to the login page
5. Log in with your new credentials

### Logging In

1. Enter your username and password
2. Click **"🔓 Login"**
3. You'll be directed to the main dashboard

## Profile Settings

After logging in, you can manage your profile through the **"⚙️ Profile Settings"** tab in the sidebar:

### Update Your Information
- **Full Name**: Edit your full name
- **Skills**: Add or update your skills (comma-separated)
  - Example: `Python, Data Analysis, Machine Learning, SQL`
- **Preferred Duration**: Select your preferred internship length
  - Options: 1 month, 3 months, 6 months, 1 year, or Flexible
- **Interests**: Add or update your interests (comma-separated)
  - Example: `AI, Data Science, Web Development`

### Saving Changes
Click **"💾 Save Changes"** to update your profile. Your preferences will be saved and used for personalized opportunity recommendations.

## Using the Dashboard

### Dashboard Tab (🎓)
The Dashboard tab allows you to:

1. **Select Mode**:
   - **Existing Student**: Browse from pre-loaded student profiles
   - **Create Custom Profile**: Use your saved profile or create a temporary one

2. **Get Recommendations**:
   - For existing students: Recommendations display automatically
   - For custom profiles: Click **"🔍 Get Recommendations"** to see opportunities

3. **Filter Results**:
   - Adjust the minimum match score slider
   - Toggle expired opportunities visibility

4. **View Opportunity Details**:
   - See match percentage
   - View skill matches
   - Read AI-powered insights for why each opportunity is recommended

## File Structure

```
C:\AI_Navigator\
├── data/
│   ├── students.json          # Sample student profiles
│   ├── opportunities.json     # Available internships
│   └── users.json             # User accounts (auto-generated)
├── src/
│   ├── app.py                 # Main Streamlit application
│   ├── services/
│   │   ├── auth.py            # Authentication & user management
│   │   ├── scoring.py         # Opportunity matching algorithm
│   │   └── ai_reasoning.py    # AI insight generation
│   ├── chroma_db/
│   │   └── chroma_client.py   # Data management
│   └── utils/
│       └── helpers.py         # CSS styling
└── AUTH_GUIDE.md             # This file
```

## API Reference

### Authentication Module (`services/auth.py`)

#### `signup_user(username, email, password, full_name="")`
Create a new user account.
- **Parameters**:
  - `username` (str): Unique username
  - `email` (str): User's email address
  - `password` (str): Minimum 6 characters
  - `full_name` (str): User's full name
- **Returns**: `(bool, str)` - Success status and message

#### `login_user(username, password)`
Authenticate user credentials.
- **Parameters**:
  - `username` (str): Username
  - `password` (str): Password
- **Returns**: `(bool, dict|str)` - Success status and user data or error message

#### `get_user_profile(username)`
Retrieve user profile data.
- **Parameters**:
  - `username` (str): Username
- **Returns**: `dict` - User profile data or None

#### `update_user_profile(username, profile_data)`
Update user profile settings.
- **Parameters**:
  - `username` (str): Username
  - `profile_data` (dict): Profile dictionary with skills, interests, preferred_duration
- **Returns**: `bool` - Success status

## Security Considerations

1. **Password Hashing**: All passwords are hashed using SHA-256 before storage
2. **No Plain Text Storage**: User passwords are never stored in plain text
3. **Session State**: User authentication is managed through Streamlit session state
4. **Local Storage**: User data is stored locally in JSON format (suitable for demos; use a database for production)

## Production Deployment

For production deployment, consider:

1. **Database Integration**:
   - Replace JSON storage with a proper database (PostgreSQL, MongoDB, etc.)
   - Implement connection pooling

2. **Enhanced Security**:
   - Use bcrypt or argon2 for password hashing instead of SHA-256
   - Implement rate limiting on login attempts
   - Add email verification for new accounts

3. **Session Management**:
   - Implement JWT tokens for API authentication
   - Add session timeout
   - Implement secure cookie handling

4. **HTTPS**: Ensure all connections are encrypted with HTTPS

5. **Environment Variables**: Store sensitive configuration in environment variables

## Troubleshooting

### Issue: "Username not found!"
- **Solution**: Check spelling of username or create a new account

### Issue: "Incorrect password!"
- **Solution**: Verify your password is correct. Use the demo account if needed.

### Issue: "Username already exists!"
- **Solution**: Choose a different username for your new account

### Issue: "Email already registered!"
- **Solution**: Use a different email address or log in with your existing account

### Issue: "Password must be at least 6 characters!"
- **Solution**: Create a password with 6 or more characters

## Support

For issues or feature requests, please contact the development team or check the main application documentation.

---

**Last Updated**: December 27, 2025  
**Version**: 1.0.0
