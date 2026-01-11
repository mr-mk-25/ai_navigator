from datetime import datetime

def calculate_score(student, opp):
    matched = set(student["skills"]).intersection(set(opp["skills_required"]))
    skill_score = len(matched) / len(opp["skills_required"])
    duration_score = 1 if student["preferred_duration"] == opp["duration"] else 0
    days_left = (datetime.strptime(opp["deadline"], "%Y-%m-%d") - datetime.now()).days
    final = round((skill_score * 0.7 + duration_score * 0.3) * 100, 1)
    explanation = f"Skills matched: {len(matched)} | Duration match: {'Yes' if duration_score else 'No'} | Days left: {max(days_left,0)}"
    return final, explanation
