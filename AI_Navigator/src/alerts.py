from datetime import datetime

def is_closing_soon(deadline):
    days_left = (datetime.strptime(deadline, "%Y-%m-%d") - datetime.now()).days
    return days_left <= 7
