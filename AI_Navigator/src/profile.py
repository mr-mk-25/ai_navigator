import json

def load_student_profile():
    with open("data/students.json") as f:
        return json.load(f)
