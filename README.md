# AI Navigator
AI Internship Navigator — Complete project overview and quick-start guide

A lightweight Streamlit app that helps students find internship opportunities by matching profiles (skills, interests, preferences) to opportunities using simple scoring and AI insights. This repository contains the app code, authentication, documentation, and sample data to try the system locally.

---

## Table of contents
- [Quick Links](#quick-links)
- [Highlights](#highlights)
- [Demo account](#demo-account)
- [Quick start (30 seconds)](#quick-start-30-seconds)
- [Project structure](#project-structure)
- [Documentation & developer guides](#documentation--developer-guides)
- [Key features](#key-features)
- [Security & production recommendations](#security--production-recommendations)
- [Testing checklist](#testing-checklist)
- [Support & troubleshooting](#support--troubleshooting)
- [Next steps](#next-steps)
- [Version & stats](#version--stats)

---

## Quick Links
- Start the app: `streamlit run src/app.py`
- Local app URL: `http://localhost:8501`
- Docs:
  - QUICK_START.md — Quick user guide
  - AUTH_GUIDE.md — Detailed user & API guide
  - AUTHENTICATION_ARCHITECTURE.md — Technical architecture & security
  - AUTHENTICATION_SUMMARY.md — Implementation summary

---

## Highlights
- Streamlit-based UI with login/signup flow
- JSON-backed user storage for quick local testing
- Password hashing and session management
- Profile management + AI-backed recommendation scoring
- Documentation and architecture guides included

---

## Demo account
Use this to explore the app immediately:

```
Username: demo_user
Password: demo123

Email: demo@example.com
Full Name: Demo User
Skills: Python, Data Analysis, Machine Learning
Duration: 3 months
Interests: AI, Data Science
```

---

## Quick start (30 seconds)

1. Clone the repo (or open project folder)
2. From the repo root, create & activate your Python venv (recommended)
3. Install requirements:
   ```
   pip install -r requirements.txt
   ```
   (file is named `requirements.txt` — if your copy has a typo `requriements.txt`, please rename.)
4. Run the app:
   ```
   streamlit run src/app.py
   ```
5. Open browser at `http://localhost:8501` and log in (use demo account or sign up)

---

## Project structure
C:\AI_Navigator\ (logical layout)

- Documentation
  - QUICK_START.md
  - AUTH_GUIDE.md
  - AUTHENTICATION_ARCHITECTURE.md
  - AUTHENTICATION_SUMMARY.md
  - README.md (this file)
- src/
  - app.py — Main Streamlit application, UI & session handling
  - services/
    - auth.py — Authentication service (signup/login, password hashing)
    - scoring.py — Opportunity scoring algorithm
    - ai_reasoning.py — AI insights / recommendation helpers
  - chroma_db/
    - chroma_client.py — Data management utilities
  - utils/
    - helpers.py — Styling, CSS and UI helpers
- data/
  - users.json — User accounts (JSON-backed DB for local testing)
  - students.json — Sample student profiles
  - opportunities.json — Sample internship opportunities
- requirements.txt — Python dependencies

---

## Documentation & developer guides
- AUTHENTICATION_ARCHITECTURE.md — System diagrams, component details, DB migration guidance, production recommendations
- AUTH_GUIDE.md — Detailed user guide: features, account/profile usage, API reference
- AUTHENTICATION_SUMMARY.md — What was created, file list, usage notes, and next steps

If you're a developer, start with AUTHENTICATION_ARCHITECTURE.md, then read `src/services/auth.py` to understand implementation details.

---

## Key features

Authentication
- Sign up with email & password
- Secure login with session management
- Password hashing (current impl: SHA-256 for local demo)

Profile management
- Create/edit user profiles
- Save skills, interests, preferences
- Persistent JSON storage for quick testing

User interface
- Professional login / signup screens
- Sidebar profile settings
- Dashboard with recommendations and match scores
- Logout functionality

Security (local/demo)
- Passwords are hashed before storage
- Session state is used to isolate users
- Basic input validation and error handling

---

## Security & production recommendations
The current demo uses a JSON-backed store and SHA-256 hashing (suitable for learning/demo). For production, implement:
- Strong hashing: bcrypt or Argon2
- Email verification & password reset flows
- Rate limiting and brute-force protections
- Use a real database (Postgres, MySQL, etc.) with migrations
- Enforce HTTPS/SSL and secure cookies
- Audit logging and monitoring

See AUTHENTICATION_ARCHITECTURE.md for more architecture and deployment advice.

---

## Testing checklist
- Start application and load login page
- Sign up with valid credentials
- Login with correct password
- Verify wrong password fails gracefully
- Create/update profile settings
- Logout and log in again to verify persistence
- Use demo account to test quickly
- Try invalid inputs to test validation behaviors
- Validate recommendations update when profile changes

---

## Support & troubleshooting

Common issues
- Can't start app: Ensure you run from repo root and have Streamlit installed
- Can't login: Check username/password; try demo_user demo123
- Account won't create: Check for duplicate email in `data/users.json`
- Empty recommendations: Make sure profile fields have skills/interests populated

Where to find help
- Quick answers: QUICK_START.md
- Detailed user guide: AUTH_GUIDE.md
- Technical & security: AUTHENTICATION_ARCHITECTURE.md

---

## Next steps (for users & developers)

For users
- Start app and explore with demo account
- Create your profile and view recommendations
- Provide feedback or file issues for missing features

For developers
- Review architecture docs and `src/services/auth.py`
- Add production-grade password hashing and DB support
- Add email verification & password reset flows
- Harden validation and logging
- Add automated tests and CI

---

## Version & system stats
- Version: 1.0.0
- Release date: December 27, 2025
- Framework: Streamlit
- Python: 3.8+
- Data store: JSON (demo)
- Authentication functions (approx): 6

---

## Contributing
Contributions welcome — please open issues or PRs with improvements, bug fixes, or documentation updates. If you plan to add features, open an issue first to discuss the design.

---

## License & contact
Specify project license (e.g., MIT) in a LICENSE file. For questions, open an issue or contact the repository owner.

---

Happy exploring — run:
```
streamlit run src/app.py
```
and open http://localhost:8501
