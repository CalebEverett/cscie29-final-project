from click import help_option
from django.db import models
from django.utils import timezone


class TimeStampMixin(models.Model):
    """Abstract base class to include `created_date` and `last_modified`
    fields on all models.
    """

    created_date = models.DateTimeField(
        default=timezone.now,
        help_text="Automatically populates timestamp upon creation.",
    )
    last_modified = models.DateTimeField(
        help_text="Automatically updates timestamp whenever record is modified.",
        auto_now=True,
    )

    class Meta:
        abstract = True


class Company(TimeStampMixin):
    """This model contains basic information about the organizations
    applying for grants. Separating out a separate model for a Company allows
    a single company to potentially have multiple applications.
    """

    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Name of the company in 200 characters or less.",
    )
    city = models.CharField(
        max_length=50, help_text="Name of the city in 50 characters or less."
    )
    state = models.CharField(
        max_length=50, help_text="Name of the state in 50 characters or less."
    )


class Application(TimeStampMixin):
    """Main object for grant applications. To start with this will be
    populated from a csv file with the applications submitted through
    another application. Eventually this application will be set up with
    forms to allow applications to be submitted directly through this application.
    """

    class Status(models.IntegerChoices):
        """Choices for application status. These are set up as integers
        to facilitate the use of the status as hierarchical, i.e.,
        `APPROVED` > `CREATED`.

        Parameters:
            CREATED: Created in the system, but not otherwise touched.
            PRE_REJECTED: Rejected before being sent out to reviewers for
                further evaluation.
            REVIEWS_IN_PROGRESS: Approved for review.
            REVIEWS_COMPLETED: Specified number of review have been completed.
            POST_REJECTED: Rejected based on review scores.
            APPROVED: Approved to move through to final evaluation phase.
        """

        CREATED = 100
        PRE_REJECTED = 200
        REVIEWS_IN_PROGRESS = 300
        REVIEWS_COMPLETED = 400
        POST_REJECTED = 500
        APPROVED = 600

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, help_text="Foreign key lookup to company."
    )
    status = models.IntegerField(choices=Status.choices)


class Reviewer(TimeStampMixin):
    """This is the main object for reviewers, set up for demonstration purposes as
    a separate object. Ultimately this will be based on the built in User model to
    take advantage of the authorization, permission and group functionality that
    already exists.
    """

    class Status(models.IntegerChoices):
        """Choices for reviewer status. These are set up as integers
        to facilitate the use of the status as hierarchical, i.e.,
        `ACTIVE` > `NEW`.

        Parameters:
            NEW: Created in the system, but not otherwise touched.
            ACTIVE: Eligible to be assigned to complete reviews.
            PAUSED: Qualified to complete reviews, but not eligible to
                be assigned reviews.
            INACTIVE: No longer eligible to complete reviews.
        """

        NEW = 100
        ACTIVE = 200
        PAUSED = 300
        INACTIVE = 400

    email = models.EmailField()
    status = models.IntegerField(choices=Status.choices)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)


class Question(TimeStampMixin):
    """This is the main object for a standardized question to be completed for
    all applications or all reviews of applications. Set up as an abstract
    base class to be able to share common attributes between applications and
    reviews.
    """

    class Type(models.TextChoices):
        TEXT = "TEXT"
        NUMBER = "NUMBER"

    class Status(models.TextChoices):
        DRAFT = "DRAFT"
        ACTIVE = "ACTIVE"
        INACTIVE = "INACTIVE"

    question_type = models.CharField(choices=Type.choices, max_length=25)
    status = models.CharField(choices=Status.choices, max_length=25)
    question = models.CharField(max_length=250)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.question} ({self.status})"


class ApplicationQuestion(Question):
    pass


class ApplicationAnswer(TimeStampMixin):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    question = models.ForeignKey(ApplicationQuestion, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=1000)
    answer_number = models.IntegerField()


class ReviewQuestion(Question):
    """Standard question for reviews of applications."""

    points = models.IntegerField()


class Assignment(TimeStampMixin):
    """Junction object linking a reviewer to an application."""

    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(Reviewer, on_delete=models.CASCADE)


class ReviewAnswer(TimeStampMixin):
    """Junction object linking an assignment to a review question."""

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    question = models.ForeignKey(ReviewQuestion, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=250)
    answer_score = models.IntegerField()
