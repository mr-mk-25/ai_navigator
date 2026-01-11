def calculate_score(student, opportunity):
    score = 0
    explanation = {}

    student_skills = set(student.get("skills", []))
    required_skills = set(opportunity.get("skills_required", []))

    if required_skills:
        matched_skills = student_skills.intersection(required_skills)
        skill_score = (len(matched_skills) / len(required_skills)) * 60
        score += skill_score
        explanation["skills"] = f"{len(matched_skills)} of {len(required_skills)} skills matched"
    else:
        explanation["skills"] = "No required skills listed"

    if student.get("preferred_duration") == opportunity.get("duration"):
        score += 20
        explanation["duration"] = "Preferred duration matched"
    else:
        explanation["duration"] = "Duration differs"

    student_interests = set(student.get("interests", []))
    opp_tags = set(opportunity.get("tags", []))

    if student_interests.intersection(opp_tags):
        score += 20
        explanation["interests"] = "Interest alignment found"
    else:
        explanation["interests"] = "No interest overlap"

    return round(score, 1), explanation
