def skill_match_score(student_skills, required_skills):
    matched = set(student_skills) & set(required_skills)
    return len(matched) / len(required_skills)
