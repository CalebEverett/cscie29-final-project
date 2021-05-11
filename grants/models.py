from email.mime import application
from django.db import models
from django.utils import timezone
from django.conf import settings


class TimeStampMixin(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Company(TimeStampMixin):
    name = models.CharField(max_length=200, unique=True)


class Application(TimeStampMixin):
    """Main object for grant applications."""

    class ApplicationStatus(models.IntegerChoices):
        """Choices for application status. These are set up as integers
        to facilitate the use of the status as hierarchical, i.e.,
        `APPROVED` > `CREATED`.

        Parameters:
            CREATED: Created in the system, but not otherwise touched.
            PRE_REJECTED: Rejected before being sent out to reviewers for
                further evaluation.
        """

        CREATED = 100
        PRE_REJECTED = 200
        REVIEWS_IN_PROGRESS = 300
        REVIEWS_COMPLETED = 400
        POST_REJECTED = 500
        APPROVED = 600

    company = models.ForeignKey("Company", on_delete=models.PROTECT)
    status = models.IntegerField(choices=ApplicationStatus.choices)


class Reviewer(models.Model):
    class ReviewerStatus(models.IntegerChoices):
        NEW = 100
        ACTIVE = 200
        PAUSED = 300
        INACTIVE = 400

    email = models.EmailField(primary_key=True)
    status = models.IntegerField(choices=ReviewerStatus.choices)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)


class Question(TimeStampMixin):
    class QuestionType(models.TextChoices):
        TEXT = "TEXT"
        NUMBER = "NUMBER"

    class QuestionStatus(models.TextChoices):
        DRAFT = "DRAFT"
        ACTIVE = "ACTIVE"
        INACTIVE = "INACTIVE"

    question_type = models.CharField(choices=QuestionType.choices, max_length=25)
    status = models.CharField(choices=QuestionStatus.choices, max_length=25)
    question = models.CharField(max_length=250)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.question} ({self.status})"


class ApplicationQuestion(Question):
    pass


class ApplicationAnswer(TimeStampMixin):
    application = models.ForeignKey(Application, on_delete=models.PROTECT)
    question = models.ForeignKey(ApplicationQuestion, on_delete=models.PROTECT)
    answer_text = models.CharField(max_length=1000)
    answer_number = models.IntegerField()


class ReviewQuestion(Question):
    points = models.IntegerField()


class Assignment(TimeStampMixin):
    application = models.ForeignKey(Application, on_delete=models.PROTECT)
    reviewer = models.ForeignKey(Reviewer, on_delete=models.PROTECT)


class ReviewAnswer(TimeStampMixin):
    assignment = models.ForeignKey(Assignment, on_delete=models.PROTECT)
    question = models.ForeignKey(ReviewQuestion, on_delete=models.PROTECT)
    answer_text = models.CharField(max_length=250)
    answer_score = models.IntegerField()
