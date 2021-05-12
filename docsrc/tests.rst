=======================
Tests
=======================

The abstract base test class skinnined the tests for the creation and loading of four fixtures down to three lines each. In addition to designing the classes and the tests so they could be repeated that concisely, another key to making that work is the :code:`__test__` parameter. Setting that to :code:`False` on the abstract base class prevents it from being discovered by pytest. Then on the instances that we want to test, we just set it to :code:`True`.

::

    class LoadTableTests(DJTest):
        """Abstract base class to test creation of fixture and load to designated table."""

        __test__ = False
        fixture_task: Task
        table_task: Task
        sample_size: int = 10

        def test_fixture(self):
            with TemporaryDirectory() as tmp:
                create_fixture = self.fixture_task(
                    sample_size=self.sample_size, parent_dir=tmp
                )

                result = build(
                    [create_fixture],
                    detailed_summary=True,
                    local_scheduler=True,
                )

                with create_fixture.output().open() as f:
                    fields = []
                    for line in f:
                        fields.append(json.loads(line)["fields"])

                df = pd.DataFrame(fields)

                print(df.iloc[0].to_dict())
                self.assertEqual(Path(create_fixture.output().path).parent, Path(tmp))
                self.assertEqual(result.status, SUCCESS)
                self.assertEqual(len(df), 10)
                self.assertFalse(df.isna().any().any())

            self.assertFalse(Path(tmp).exists())

        def test_table(self):
            with TemporaryDirectory() as tmp:
                load_table = self.table_task(parent_dir=tmp, sample_size=self.sample_size)

                result = build(
                    [load_table],
                    detailed_summary=True,
                    local_scheduler=True,
                )

            self.assertEqual(
                load_table.output().model.objects.count(), load_table.sample_size
            )
            self.assertEqual(result.status, SUCCESS)


    class LoadCompanyTests(LoadTableTests):
        __test__ = True
        fixture_task = CompanyFixtureTask
        table_task = CompanyTableTask


    class LoadApplicationTests(LoadTableTests):
        __test__ = True
        fixture_task = ApplicationFixtureTask
        table_task = ApplicationTableTask


    class LoadApplicationTests(LoadTableTests):
        __test__ = True
        fixture_task = ApplicationFixtureTask
        table_task = ApplicationTableTask


    class LoadReviewerTests(LoadTableTests):
        __test__ = True
        fixture_task = ReviewerFixtureTask
        table_task = ReviewerTableTask


    class AllTableTests(DJTest):
        """Ensure that all tables are loaded successfully."""

        def test_all_tables(self):
            with TemporaryDirectory() as tmp:
                load_table = AllTablesTask(parent_dir=tmp, sample_size=10)

                result = build(
                    [load_table],
                    detailed_summary=True,
                    local_scheduler=True,
                )

            self.assertEqual(result.status, SUCCESS)
            print(load_table.input())
            for table, target in load_table.input().items():
                with self.subTest(table=table):
                    self.assertEqual(target.model.objects.count(), load_table.sample_size)

        def test_load_sample_data(self):
            """Ensure that management command to load sample data functions correctly."""

            sample_size = 10

            with TemporaryDirectory() as tmp:

                call_command(
                    "load_sample_data",
                    "--parent_dir",
                    tmp,
                    "--sample_size",
                    sample_size,
                    "--force",
                    "yes",
                )

            for model in [Application, Company, Reviewer]:
                with self.subTest(model=model.__name__):
                    self.assertEqual(model.objects.count(), sample_size)