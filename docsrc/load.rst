================
Load Sample Data
================

Here is the custom :code:`load_sample_data` management command. In the end, it all boils down to the single :code:`AllTablesTask`, but there is a lot that is accomplished with that single task. A few of the implementation details are covered in :doc:`Tasks <tasks>`, but a couple of nice design features worth mentioning here include:

* Command line argument to :option:`--force` overwriting of existing fixtures
* Relies on atomic nature of built in django :code:`loaddata` command to delete existing data for clean reinstallation
* Breaking out :option:`--parent_dir` allows testing in temporary directory
* Using luigi's text completion message to feed to django's styled standard out keeps things tight
* Fixture files are written in jsonl, which wile not necessary for the size of this sample data, are a useful format because unlike regular json, they can be read one line at a time, conserving memory and facilitating the loading of extremely large files.


::

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
            """Loads sample data from random-data-api.com"""

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


Command Line Options
--------------------
..  option:: --force <bool>, Forces overwriting of any existing fixture files
..  option:: --parent_dir <str>, Parent directory where fixture files will be written
..  option:: --sample_size <int>, Controls how many sample records are created for each model