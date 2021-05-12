import os
from typing import Dict, List

from canvasapi.quiz import QuizSubmissionQuestion
from csci_utils.canvas_utils import SubmissionManager
from git import Repo

REPO = Repo(".")


if __name__ == "__main__":
    url = os.getenv("CANVAS_URL")
    token = os.getenv("CANVAS_TOKEN")

    sm = SubmissionManager(
        assignment_name="Final Project",
        quiz_name=None,
        canvas_url=url,
        canvas_token=token,
    )

    sm.get_canvas_objects()
    sm.assignment_submit(verbose=True)
