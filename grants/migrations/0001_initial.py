# Generated by Django 3.2 on 2021-05-01 01:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Application",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("last_modified", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (100, "Created"),
                            (200, "Pre Rejected"),
                            (300, "Reviews In Progress"),
                            (400, "Reviews Completed"),
                            (500, "Post Rejected"),
                            (600, "Approved"),
                        ]
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ApplicationQuestion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("last_modified", models.DateTimeField(auto_now=True)),
                (
                    "question_type",
                    models.CharField(
                        choices=[("TEXT", "Text"), ("NUMBER", "Number")], max_length=25
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("DRAFT", "Draft"),
                            ("ACTIVE", "Active"),
                            ("INACTIVE", "Inactive"),
                        ],
                        max_length=25,
                    ),
                ),
                ("question", models.CharField(max_length=250)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Assignment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("last_modified", models.DateTimeField(auto_now=True)),
                (
                    "application",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="grants.application",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=200, unique=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Reviewer",
            fields=[
                (
                    "email",
                    models.EmailField(
                        max_length=254, primary_key=True, serialize=False
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (100, "New"),
                            (200, "Active"),
                            (300, "Paused"),
                            (400, "Inactive"),
                        ]
                    ),
                ),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="ReviewQuestion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("last_modified", models.DateTimeField(auto_now=True)),
                (
                    "question_type",
                    models.CharField(
                        choices=[("TEXT", "Text"), ("NUMBER", "Number")], max_length=25
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("DRAFT", "Draft"),
                            ("ACTIVE", "Active"),
                            ("INACTIVE", "Inactive"),
                        ],
                        max_length=25,
                    ),
                ),
                ("question", models.CharField(max_length=250)),
                ("points", models.IntegerField()),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ReviewAnswer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("answer_text", models.CharField(max_length=250)),
                ("answer_score", models.IntegerField()),
                (
                    "assignment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="grants.assignment",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="grants.reviewquestion",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="assignment",
            name="reviewer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="grants.reviewer"
            ),
        ),
        migrations.CreateModel(
            name="ApplicationAnswer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("answer_text", models.CharField(max_length=1000)),
                ("answer_number", models.IntegerField()),
                (
                    "application",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="grants.application",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="grants.applicationquestion",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="application",
            name="company",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="grants.company"
            ),
        ),
    ]
