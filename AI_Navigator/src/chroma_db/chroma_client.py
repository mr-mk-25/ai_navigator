import json
import os
from pathlib import Path
from datetime import datetime

# Initialize data storage
opportunities_data = []
students_data = []

def load_initial_data():
    """Load opportunities and students data from JSON files."""
    global opportunities_data, students_data
    
    # Get the parent directory of the src folder
    src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    parent_dir = os.path.dirname(src_dir)
    opp_path = os.path.join(parent_dir, "data", "opportunities.json")
    students_path = os.path.join(parent_dir, "data", "students.json")
    
    if os.path.exists(opp_path):
        with open(opp_path, "r", encoding="utf-8") as f:
            opportunities_data = json.load(f)
    
    if os.path.exists(students_path):
        with open(students_path, "r", encoding="utf-8") as f:
            students_data = json.load(f)

def search_opportunities(student, limit=None):
    """
    Search and rank opportunities based on student profile.
    Uses comprehensive scoring: skill matching, duration, deadline urgency.
    """
    if not opportunities_data:
        load_initial_data()
    
    ranked = []
    student_skills = set(student.get("skills", []))
    student_interests = set(student.get("interests", []))
    preferred_duration = student.get("preferred_duration", "")
    
    for opp in opportunities_data:
        required_skills = set(opp.get("skills_required", []))
        
        # 1. SKILL MATCH SCORE (50% weight)
        # Calculate the percentage of required skills the student has
        if required_skills:
            matched = student_skills.intersection(required_skills)
            skill_score = len(matched) / len(required_skills)
        else:
            skill_score = 0.7
        
        # 2. DURATION MATCH SCORE (30% weight)
        # Perfect match gives 1.0, no duration info gives 0.7, mismatch gives 0.5
        opp_duration = opp.get("duration", "")
        if opp_duration == preferred_duration:
            duration_score = 1.0
        elif not opp_duration:
            duration_score = 0.7
        else:
            duration_score = 0.5
        
        # 3. DEADLINE URGENCY SCORE (20% weight)
        deadline = opp.get("deadline", "")
        urgency_score = 0.4  # Default for missing deadline
        if deadline:
            try:
                deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
                days_left = (deadline_date - datetime.now()).days
                
                if days_left < 0:
                    urgency_score = 0.2  # Expired - low score but still show
                elif days_left <= 3:
                    urgency_score = 1.0  # Very urgent
                elif days_left <= 7:
                    urgency_score = 0.9
                elif days_left <= 15:
                    urgency_score = 0.8
                elif days_left <= 30:
                    urgency_score = 0.7
                else:
                    urgency_score = 0.5
            except:
                urgency_score = 0.4
        
        # Calculate final weighted score
        final_score = (skill_score * 0.5) + (duration_score * 0.3) + (urgency_score * 0.2)
        
        ranked.append({
            **opp,
            "score": final_score,
            "matched_skills": list(student_skills.intersection(required_skills)),
            "required_skills": list(required_skills),
            "skill_match_score": skill_score,
            "duration_score": duration_score,
            "urgency_score": urgency_score
        })
    
    # Sort by score (descending) and by matched skills count (tie-breaker)
    ranked.sort(key=lambda x: (x["score"], len(x["matched_skills"])), reverse=True)
    
    # Return all results if limit is None, otherwise return limited results
    if limit:
        return ranked[:limit]
    return ranked

def get_all_opportunities():
    """Get all opportunities."""
    if not opportunities_data:
        load_initial_data()
    return opportunities_data

def get_all_students():
    """Get all students."""
    if not students_data:
        load_initial_data()
    return students_data

# Initialize data storage
opportunities_data = None
students_data = None
