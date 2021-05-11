from csci_utils.cli import str2bool
from django.core.management import BaseCommand
from luigi import build

from ._tasks import AllTablesTask


class Command(BaseCommand):
    help = "Load sample data."

    def add_arguments(self, parser):

        parser.add_argument(
            "--force",
            type=str2bool,
            nargs="?",
            const=True,
            default=False,
            help="Force overwrite of existing fixtures.",
        )

        parser.add_argument(
            "--sample_size",
            type=int,
            default=10,
            help="Number of sample records to create for each table.",
        )

        parser.add_argument(
            "--parent_dir",
            type=str,
            default="grants/fixtures",
            help="Parent directory to write fixture files to.",
        )

    def handle(self, *args, **options):
        """Populates the DB with review aggregations"""

        force = options["force"]
        sample_size = options["sample_size"]
        parent_dir = options["parent_dir"]

        result = build(
            [
                AllTablesTask(
                    force=force,
                    sample_size=sample_size,
                    parent_dir=parent_dir,
                )
            ],
            detailed_summary=True,
            local_scheduler=True,
        )

        self.stdout.write(self.style.SUCCESS(result.one_line_summary))
