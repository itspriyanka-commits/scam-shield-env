def grade(task, action):
    score = 0.0
    feedback = []

    correct = (action.is_scam and task["label"] == "scam") or \
              (not action.is_scam and task["label"] == "not_scam")

    if correct:
        score += 0.4
    else:
        feedback.append("Incorrect scam detection")

    if action.scam_type == task["type"]:
        score += 0.2

    explanation = action.explanation.lower()
    if any(word in explanation for word in ["urgent", "link", "reward", "verify", "bank", "upi", "customs"]):
        score += 0.2
    else:
        feedback.append("Weak explanation")

    advice = action.advice.lower()
    if any(word in advice for word in ["do not click", "official", "contact", "do not share", "ignore"]):
        score += 0.2
    else:
        feedback.append("Weak advice")

    score = max(0.0, min(score, 1.0))
    return score, "; ".join(feedback)