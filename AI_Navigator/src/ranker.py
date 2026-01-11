from datetime import datetime

def rank_opportunities(student, opportunities):
    ranked = []

    for opp in opportunities:
        score = skill_match_score(
            student["skills"],
            opp["skills_required"]
        )

        # Bonus if duration matches
        if opp.get("duration") == student["preferred_duration"]:
            score += 0.2

        ranked.append((opp, score))

    return sorted(ranked, key=lambda x: x[1], reverse=True)
