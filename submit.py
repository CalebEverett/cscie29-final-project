import os
from typing import Dict, List

import final_project
from canvasapi.quiz import QuizSubmissionQuestion
from csci_utils.canvas_utils import SubmissionManager
from git import Repo

REPO = Repo(".")

def answers_fn(questions: List[QuizSubmissionQuestion]) -> List[Dict]:
    """Returns answers to Canvas quiz questions."""

    answers = [dict(id=q.id, answer=q.answer) for q in questions]

    # Question 1
    for k in questions[0].answer.keys():
        answers[0]["answer"][k] = 42

    # Question 4
    answers[2]["answer"] = REPO.head.commit.hexsha[:8]

    # Question 3
    if REPO.is_dirty():
        answers[3]["answer"] = 5153
    else:
        answers[3]["answer"] = 4031

    return answers


if __name__ == "__main__":
    url = os.getenv("CANVAS_URL")
    token = os.getenv("CANVAS_TOKEN")

    sm = SubmissionManager(
        assignment_name="Final Project",
        quiz_name="Final Project Answers",
        min_quiz_score=10,
        canvas_url=url,
        canvas_token=token,
    )

    sm.get_canvas_objects()
    sm.print_quiz_questions()
