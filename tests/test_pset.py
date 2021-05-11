#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import json
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd
from django.core.management import call_command
from django.forms.models import model_to_dict
from django.test import TestCase as DJTest
from luigi import build, execution_summary

from grants.models import Application, Company
from grants.management.commands._tasks import (
    ApplicationFixtureTask,
    ApplicationTableTask,
    CompanyFixtureTask,
    CompanyTableTask,
)

SUCCESS = execution_summary.LuigiStatusCode.SUCCESS


class LoadCompanyTests(DJTest):
    def test_fixture(self):
        with TemporaryDirectory() as tmp:
            create_fixture = CompanyFixtureTask(sample_size=10, parent_dir=tmp)

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
            load_table = CompanyTableTask(parent_dir=tmp, sample_size=10)

            result = build(
                [load_table],
                detailed_summary=True,
                local_scheduler=True,
            )

        self.assertEqual(Company.objects.count(), load_table.sample_size)
        self.assertEqual(result.status, SUCCESS)


class LoadApplicationTests(DJTest):
    def test_fixture(self):
        with TemporaryDirectory() as tmp:
            create_fixture = ApplicationFixtureTask(sample_size=10, parent_dir=tmp)

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
            load_table = ApplicationTableTask(parent_dir=tmp, sample_size=10)

            result = build(
                [load_table],
                detailed_summary=True,
                local_scheduler=True,
            )

        self.assertEqual(Application.objects.count(), load_table.sample_size)
        self.assertEqual(result.status, SUCCESS)
