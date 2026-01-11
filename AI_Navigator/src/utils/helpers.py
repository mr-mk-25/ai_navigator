import streamlit as st

def load_css():
    """Load dark mode CSS styling with enhanced UI/UX."""
    st.markdown("""
    <style>
    /* Dark mode theme */
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    body {
        background-color: #020617;
        color: #E2E8F0;
    }

    .stApp {
        background-color: #020617;
    }

    /* Main container styling */
    .main {
        padding: 20px;
    }

    /* Card styling with hover effect */
    .card {
        background: linear-gradient(135deg, #0F172A 0%, #1A2332 100%);
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #4F46E5;
        box-shadow: 0px 8px 32px rgba(0,0,0,0.5);
        margin-bottom: 25px;
        color: #E2E8F0;
        transition: all 0.3s ease;
    }

    .card:hover {
        box-shadow: 0px 12px 40px rgba(79, 70, 229, 0.3);
        transform: translateY(-2px);
    }

    /* Heading styles */
    h1 {
        color: #F1F5F9;
        font-size: 2.5em;
        font-weight: 700;
        margin-bottom: 20px;
        text-shadow: 0 2px 10px rgba(79, 70, 229, 0.2);
    }

    h2, h3 {
        color: #F1F5F9;
        font-weight: 600;
    }

    h2 {
        font-size: 1.8em;
    }

    h3 {
        font-size: 1.4em;
    }

    /* Score styling with glow effect */
    .score {
        font-size: 28px;
        font-weight: bold;
        color: #22C55E;
        margin: 15px 0;
        text-shadow: 0 0 15px rgba(34, 197, 94, 0.4);
        letter-spacing: 1px;
    }

    /* Reason box styling */
    .reason {
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.15) 0%, rgba(79, 70, 229, 0.05) 100%);
        padding: 18px;
        border-radius: 12px;
        border-left: 4px solid #4F46E5;
        margin-top: 15px;
        line-height: 1.9;
        color: #CBD5E1;
        backdrop-filter: blur(10px);
    }

    /* Badge styling */
    .badge {
        display: inline-block;
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        color: #F1F5F9;
        padding: 8px 14px;
        border-radius: 8px;
        margin-right: 10px;
        font-size: 12px;
        margin-bottom: 12px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .badge-expired {
        background: linear-gradient(135deg, #DC2626 0%, #EF4444 100%);
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.4);
    }

    .badge-secondary {
        background: linear-gradient(135deg, #22C55E 0%, #4ADE80 100%);
        box-shadow: 0 4px 12px rgba(34, 197, 94, 0.4);
    }

    .badge-accent {
        background: linear-gradient(135deg, #F97316 0%, #FB923C 100%);
        box-shadow: 0 4px 12px rgba(249, 115, 22, 0.4);
    }

    /* Sidebar styling */
    .sidebar {
        background-color: #0F172A;
        border-right: 1px solid #1A2332;
    }

    /* Text styling */
    p {
        color: #CBD5E1;
        line-height: 1.7;
    }

    /* Input styling */
    .stSelectbox, .stSlider, .stCheckbox, .stTextInput {
        color: #E2E8F0;
    }

    .stSelectbox label, .stSlider label, .stCheckbox label, .stTextInput label {
        color: #F1F5F9 !important;
        font-weight: 600;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        color: #F1F5F9;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 1.1em;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
    }

    .stButton > button:hover {
        box-shadow: 0 6px 25px rgba(79, 70, 229, 0.5);
        transform: translateY(-2px);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* Metric styling */
    .stMetric {
        background: linear-gradient(135deg, #0F172A 0%, #1A2332 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 4px solid #4F46E5;
        text-align: center;
    }

    .stMetric label {
        color: #CBD5E1 !important;
    }

    /* Alert styling */
    .stAlert {
        border-radius: 12px;
        border-left: 5px solid;
    }

    /* Info box */
    [data-testid="stAlert"] {
        background-color: rgba(79, 70, 229, 0.1);
        border-color: #4F46E5;
    }

    /* Success message */
    .stSuccess {
        background-color: rgba(34, 197, 94, 0.1) !important;
        border-color: #22C55E !important;
    }

    /* Warning message */
    .stWarning {
        background-color: rgba(249, 115, 22, 0.1) !important;
        border-color: #F97316 !important;
    }

    /* Smooth transitions */
    * {
        transition: background-color 0.3s ease, color 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)

