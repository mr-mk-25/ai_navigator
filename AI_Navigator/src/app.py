import streamlit as st
import json
import os
from datetime import datetime
import hashlib

# ---------------------------
# Path Setup
# ---------------------------
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

STUDENT_FILE = os.path.join(DATA_DIR, "students.json")
OPPORTUNITY_FILE = os.path.join(DATA_DIR, "opportunities.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")

# Create users.json if it doesn't exist
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

# ---------------------------
# User Management Functions
# ---------------------------
def hash_password(password):
    """Hash password for security"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Load all users from users.json"""
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            users = json.load(f)
            return users if isinstance(users, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_users(users):
    """Save users to users.json"""
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving users: {e}")
        return False

def user_exists(username):
    """Check if username already exists"""
    users = load_users()
    return any(user.get("username") == username for user in users)

def authenticate_user(username, password):
    """Authenticate user credentials"""
    users = load_users()
    for user in users:
        if user.get("username") == username:
            if user.get("password") == hash_password(password):
                return True, user
            return False, "Incorrect password"
    return False, "User not found"

def create_user(username, email, full_name, password):
    """Create a new user"""
    if user_exists(username):
        return False, "Username already exists"
    
    users = load_users()
    new_user = {
        "user_id": len(users) + 1,
        "username": username,
        "email": email,
        "full_name": full_name,
        "password": hash_password(password),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "profile": {
            "skills": [],
            "interests": [],
            "preferred_duration": "3 months"
        }
    }
    users.append(new_user)
    return save_users(users), "User created successfully"

def load_student_profile():
    """Load and return the first student from students.json"""
    try:
        with open(STUDENT_FILE, "r", encoding="utf-8") as f:
            students = json.load(f)
            if isinstance(students, list) and students:
                return students[0]
            elif isinstance(students, dict):
                return students
            else:
                return {}
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return {}

def load_opportunities():
    """Load opportunities from opportunities.json"""
    try:
        with open(OPPORTUNITY_FILE, "r", encoding="utf-8") as f:
            opps = json.load(f)
            if isinstance(opps, list):
                return opps
            else:
                return [opps] if isinstance(opps, dict) else []
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return []

def skill_match_score(student_skills, required_skills):
    """Calculate skill match score between student and opportunity"""
    if not required_skills:
        return 0.0
    matched = set(student_skills).intersection(set(required_skills))
    return len(matched) / len(required_skills)

def is_closing_soon(deadline):
    """Check if opportunity is closing within 7 days"""
    try:
        days_left = (datetime.strptime(deadline, "%Y-%m-%d") - datetime.now()).days
        return days_left <= 7, days_left
    except ValueError:
        return False, -1

def rank_opportunities(student, opp_data):
    """Rank opportunities based on skill match and other factors"""
    ranked = []
    
    if not isinstance(student, dict) or not isinstance(opp_data, list):
        return ranked

    for opp in opp_data:
        if not isinstance(opp, dict):
            continue
        
        required_skills = opp.get("skills_required") or opp.get("skills") or []
        student_skills = student.get("skills", [])
        
        score = skill_match_score(student_skills, required_skills)

        if opp.get("duration") == student.get("preferred_duration"):
            score += 0.2

        closing_soon, days_left = is_closing_soon(opp.get("deadline", "2099-12-31"))

        ranked.append({
            "title": opp.get("title", "Untitled Opportunity"),
            "type": opp.get("type", "Internship"),
            "skills_required": required_skills,
            "deadline": opp.get("deadline", "N/A"),
            "days_left": days_left,
            "closing_soon": closing_soon,
            "score": round(score, 2)
        })

    return sorted(ranked, key=lambda x: x["score"], reverse=True)

# ---------------------------
# Streamlit Configuration
# ---------------------------
st.set_page_config(
    page_title="AI Internship Navigator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "user_data" not in st.session_state:
    st.session_state.user_data = None

# Custom CSS for better styling
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3f 50%, #0f0f23 100%);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Authentication Page
# ---------------------------
if not st.session_state.authenticated:
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    with col_center:
        st.markdown("""
        <div style='text-align: center; margin-bottom: 40px;'>
            <div style='font-size: 4em; margin-bottom: 10px;'>🚀</div>
            <h1 style='color: #4F46E5; font-size: 2.5em; margin: 0;'>AI Internship Navigator</h1>
            <p style='color: #a1a1a1; font-size: 1.1em; margin: 10px 0;'>Your Smart Career Partner</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Features showcase
        st.markdown("""
        <div style='
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 15px;
            margin-bottom: 40px;
        '>
            <div style='
                background: rgba(79, 70, 229, 0.1);
                border: 1px solid rgba(79, 70, 229, 0.3);
                border-radius: 12px;
                padding: 20px;
                text-align: center;
            '>
                <div style='font-size: 2em; margin-bottom: 10px;'>🤖</div>
                <div style='color: #4F46E5; font-weight: 700; margin-bottom: 5px;'>AI Powered</div>
                <div style='color: #a1a1a1; font-size: 0.85em;'>Smart Matching</div>
            </div>
            <div style='
                background: rgba(79, 70, 229, 0.1);
                border: 1px solid rgba(79, 70, 229, 0.3);
                border-radius: 12px;
                padding: 20px;
                text-align: center;
            '>
                <div style='font-size: 2em; margin-bottom: 10px;'>⚡</div>
                <div style='color: #4F46E5; font-weight: 700; margin-bottom: 5px;'>Lightning Fast</div>
                <div style='color: #a1a1a1; font-size: 0.85em;'>Instant Results</div>
            </div>
            <div style='
                background: rgba(79, 70, 229, 0.1);
                border: 1px solid rgba(79, 70, 229, 0.3);
                border-radius: 12px;
                padding: 20px;
                text-align: center;
            '>
                <div style='font-size: 2em; margin-bottom: 10px;'>🎯</div>
                <div style='color: #4F46E5; font-weight: 700; margin-bottom: 5px;'>95% Accuracy</div>
                <div style='color: #a1a1a1; font-size: 0.85em;'>Perfect Matches</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Authentication tabs
        auth_mode = st.radio(
            "Choose an option",
            ["🔓 Login", "✨ Create Account"],
            horizontal=True
        )
        
        if "Login" in auth_mode:
            # Login Form
            st.markdown("<h3 style='color: #4F46E5; text-align: center;'>Welcome Back</h3>", unsafe_allow_html=True)
            
            login_username = st.text_input(
                "Username or Email",
                placeholder="Enter your username or email",
                key="login_user"
            )
            login_password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="login_pass"
            )
            
            if st.button("🔓 Login", use_container_width=True, key="login_btn"):
                if login_username and login_password:
                    success, result = authenticate_user(login_username, login_password)
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.username = login_username
                        st.session_state.user_data = result
                        st.success("✅ Login successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error(f"❌ {result}")
                else:
                    st.error("❌ Please enter both username and password")
            
            st.markdown("---")
            st.markdown("""
            <div style='text-align: center; color: #a1a1a1;'>
                <p>Don't have an account? <span style='color: #4F46E5; font-weight: 600;'>Create one below</span></p>
            </div>
            """, unsafe_allow_html=True)
        
        else:
            # Sign Up Form
            st.markdown("<h3 style='color: #4F46E5; text-align: center;'>Create Your Account</h3>", unsafe_allow_html=True)
            
            signup_fullname = st.text_input(
                "Full Name",
                placeholder="Your full name",
                key="signup_fullname"
            )
            signup_email = st.text_input(
                "Email Address",
                placeholder="your.email@example.com",
                key="signup_email"
            )
            signup_username = st.text_input(
                "Username",
                placeholder="Choose a unique username",
                key="signup_user"
            )
            
            if signup_username:
                if user_exists(signup_username):
                    st.error("⚠️ Username already taken")
                else:
                    st.success("✅ Username available")
            
            signup_password = st.text_input(
                "Password",
                type="password",
                placeholder="At least 8 characters",
                key="signup_pass"
            )
            signup_confirm = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Confirm your password",
                key="signup_confirm"
            )
            
            # Password strength indicator
            if signup_password:
                strength = len(signup_password)
                if strength < 6:
                    st.warning("⚠️ Weak password (at least 8 characters recommended)")
                elif strength < 10:
                    st.info("👍 Fair password strength")
                else:
                    st.success("🔒 Strong password")
            
            if st.button("✨ Create Account", use_container_width=True, key="signup_btn"):
                if not all([signup_fullname, signup_email, signup_username, signup_password]):
                    st.error("❌ Please fill in all fields")
                elif signup_password != signup_confirm:
                    st.error("❌ Passwords do not match")
                elif len(signup_password) < 8:
                    st.error("❌ Password must be at least 8 characters")
                else:
                    success, message = create_user(signup_username, signup_email, signup_fullname, signup_password)
                    if success:
                        st.success(f"✅ {message}")
                        st.info("Please login with your new account")
                    else:
                        st.error(f"❌ {message}")
            
            st.markdown("---")
            st.markdown("""
            <div style='text-align: center; color: #a1a1a1;'>
                <p>Already have an account? <span style='color: #4F46E5; font-weight: 600;'>Login above</span></p>
            </div>
            """, unsafe_allow_html=True)

# ---------------------------
# Dashboard (Authenticated)
# ---------------------------
else:
    # Sidebar with user info and logout
    with st.sidebar:
        st.markdown("""
        <div style='
            background: linear-gradient(135deg, rgba(79, 70, 229, 0.1) 0%, rgba(124, 58, 237, 0.05) 100%);
            border: 1px solid rgba(79, 70, 229, 0.3);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 20px;
            text-align: center;
        '>
            <div style='color: #a1a1a1; font-size: 0.9em;'>Logged in as</div>
            <div style='color: #4F46E5; font-weight: bold; font-size: 1.1em;'>👤 {username}</div>
        </div>
        """.format(username=st.session_state.username), unsafe_allow_html=True)
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.user_data = None
            st.rerun()
        
        st.markdown("---")
        
        # Initialize student profile mode in session state
        if "profile_mode" not in st.session_state:
            st.session_state.profile_mode = "existing"
        if "custom_skills" not in st.session_state:
            st.session_state.custom_skills = ""
        if "custom_interests" not in st.session_state:
            st.session_state.custom_interests = ""
        if "custom_duration" not in st.session_state:
            st.session_state.custom_duration = "3 months"
        
        st.header("👩‍🎓 Student Profile")
        
        # Mode Selection
        st.markdown("<p style='color: #a1a1a1; margin-bottom: 10px;'><b>Select Mode:</b></p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Existing Student", use_container_width=True, 
                        key="existing_btn",
                        type="primary" if st.session_state.profile_mode == "existing" else "secondary"):
                st.session_state.profile_mode = "existing"
                st.rerun()
        
        with col2:
            if st.button("Create Custom", use_container_width=True,
                        key="custom_btn",
                        type="primary" if st.session_state.profile_mode == "custom" else "secondary"):
                st.session_state.profile_mode = "custom"
                st.rerun()
        
        st.markdown("---")
        
        # Profile Mode Selection
        if st.session_state.profile_mode == "existing":
            st.markdown("<h4 style='color: #4F46E5;'>📚 Select from Existing</h4>", unsafe_allow_html=True)
            
            # Load all students
            all_students = load_opportunities()  # This loads from students.json
            try:
                with open(os.path.join(DATA_DIR, "students.json"), "r", encoding="utf-8") as f:
                    student_list = json.load(f)
                    if isinstance(student_list, list):
                        student_names = [s.get("name", "Unknown") for s in student_list]
                    else:
                        student_names = ["Profile 1"]
            except:
                student_names = ["Profile 1", "Profile 2", "Profile 3"]
            
            selected_student_idx = st.selectbox(
                "Choose a student profile:",
                range(len(student_names)),
                format_func=lambda x: student_names[x],
                key="student_select"
            )
            
            # Load selected student
            try:
                with open(os.path.join(DATA_DIR, "students.json"), "r", encoding="utf-8") as f:
                    student_list = json.load(f)
                    if isinstance(student_list, list):
                        current_student = student_list[selected_student_idx]
                    else:
                        current_student = student_list
            except:
                current_student = {}
            
            st.markdown("<h4 style='color: #4F46E5; margin-top: 20px;'>📋 Current Profile Summary</h4>", unsafe_allow_html=True)
            
            # Display selected student info
            with st.container(border=True):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write("**Name:**")
                    st.write(current_student.get('name', 'N/A'))
                    st.write("**Academic Year:**")
                    st.write(current_student.get('academic_year', 'N/A'))
                
                with col_b:
                    st.write("**Skills:**")
                    st.write(', '.join(current_student.get('skills', [])) or "None")
                    st.write("**Interests:**")
                    st.write(', '.join(current_student.get('interests', [])) or "None")
                
                st.write("**Duration:**")
                st.write(current_student.get('preferred_duration', 'N/A'))
        
        else:  # Custom Profile Mode
            st.markdown("<h4 style='color: #4F46E5;'>✨ Create Your Profile</h4>", unsafe_allow_html=True)
            
            st.markdown("<p style='color: #a1a1a1; font-size: 0.9em; margin-top: 15px;'>Enter your skills (comma-separated):</p>", unsafe_allow_html=True)
            skills_input = st.text_input(
                "Skills",
                value=st.session_state.custom_skills,
                placeholder="Python, Deep Learning, SQL",
                label_visibility="collapsed",
                key="skills_input"
            )
            st.session_state.custom_skills = skills_input
            
            st.markdown("<p style='color: #a1a1a1; font-size: 0.9em; margin-top: 10px;'>Preferred Duration:</p>", unsafe_allow_html=True)
            duration_select = st.selectbox(
                "Duration",
                ["1 month", "2 months", "3 months", "4 months", "6 months"],
                index=2,
                label_visibility="collapsed",
                key="duration_select"
            )
            st.session_state.custom_duration = duration_select
            
            st.markdown("<p style='color: #a1a1a1; font-size: 0.9em; margin-top: 10px;'>Your interests (comma-separated):</p>", unsafe_allow_html=True)
            interests_input = st.text_input(
                "Interests",
                value=st.session_state.custom_interests,
                placeholder="Data Science, AI",
                label_visibility="collapsed",
                key="interests_input"
            )
            st.session_state.custom_interests = interests_input
            
            # Create custom profile
            custom_skills = [s.strip() for s in skills_input.split(",") if s.strip()]
            custom_interests = [i.strip() for i in interests_input.split(",") if i.strip()]
            
            current_student = {
                "name": "Custom Profile",
                "academic_year": "Your Profile",
                "skills": custom_skills,
                "interests": custom_interests,
                "preferred_duration": duration_select
            }
            
            st.markdown("<h4 style='color: #4F46E5; margin-top: 20px;'>📋 Current Profile Summary</h4>", unsafe_allow_html=True)
            
            st.markdown("<h4 style='color: #4F46E5; margin-top: 20px;'>📋 Current Profile Summary</h4>", unsafe_allow_html=True)
            
            with st.container(border=True):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write("**Name:**")
                    st.write("Custom Profile")
                    st.write("**Skills:**")
                    st.write(', '.join(custom_skills) if custom_skills else "None selected")
                
                with col_b:
                    st.write("**Interests:**")
                    st.write(', '.join(custom_interests) if custom_interests else "None selected")
                    st.write("**Duration:**")
                    st.write(duration_select)
    
    # Main content
    st.markdown("<h1 style='color: #4F46E5; text-align: center;'>🎓 AI-Assisted Internship Navigator</h1>", unsafe_allow_html=True)
    st.write("Personalized recommendations based on **skills, interests, and deadlines**")
    
    # Load data
    opportunities = load_opportunities()
    ranked_opps = rank_opportunities(current_student, opportunities)
    
    # Main Content – Opportunities
    st.subheader("🔍 Recommended Opportunities")
    
    if ranked_opps:
        for idx, opp in enumerate(ranked_opps, 1):
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"### #{idx}. {opp['title']}")
                    st.write(f"**Type:** {opp['type']}")
                    st.write(f"**Required Skills:** {', '.join(opp['skills_required'])}")
                    st.write(f"**Deadline:** {opp['deadline']}")
                    st.write("**Why recommended?**")
                    st.write(f"- Skill match score: **{opp['score']:.2f}**")
                    
                    if opp["closing_soon"]:
                        st.warning(f"⏰ Closing in {opp['days_left']} days!")
                
                with col2:
                    if opp["score"] >= 0.7:
                        st.success("🔥 High Match")
                    elif opp["score"] >= 0.4:
                        st.info("👍 Moderate Match")
                    else:
                        st.warning("⚠️ Low Match")
                
                st.divider()
    else:
        st.info("No opportunities found to match with your profile.")
    
    # Footer
    st.markdown("---")
    st.caption(
        "This AI-assisted system uses explainable rule-based intelligence to "
        "match student profiles with relevant opportunities and prioritize "
        "time-sensitive recommendations."
    )
