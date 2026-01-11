def generate_reason(student, opp, score):
    common = set(student["skills"]).intersection(set(opp["skills_required"]))
    return f"Your skills in {', '.join(common)} align strongly with this role. Overall relevance score is {score}%."
