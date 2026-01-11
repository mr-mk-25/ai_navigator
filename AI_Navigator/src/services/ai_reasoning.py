def generate_reason(student, opportunity, score):
    """
    Generate AI-powered reasoning for why an opportunity is recommended.
    """
    reasons = []
    matched_skills = opportunity.get("matched_skills", [])
    required_skills = opportunity.get("required_skills", [])
    
    # Skill-based reasoning
    if matched_skills:
        skills_str = ", ".join(matched_skills)
        reasons.append(f"Your {skills_str} skills are highly relevant")
    
    missing_skills = set(required_skills) - set(matched_skills)
    if missing_skills and len(missing_skills) <= 2:
        skills_str = ", ".join(list(missing_skills)[:2])
        reasons.append(f"Great opportunity to learn {skills_str}")
    
    # Duration reasoning
    if opportunity.get("duration") == student.get("preferred_duration"):
        reasons.append(f"Matches your {student.get('preferred_duration')} availability")
    
    # Deadline reasoning
    deadline_info = opportunity.get("deadline", "")
    if deadline_info:
        reasons.append(f"Limited time: Apply before {deadline_info}")
    
    reason_text = " • ".join(reasons) if reasons else "Strong match for your profile"
    return reason_text
