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

from grants.models import Company
from grants.management.commands._tasks import CreateCompanyFixture

SUCCESS = execution_summary.LuigiStatusCode.SUCCESS


class LoadReviewsTests(DJTest):
    def test_company_fixture(self):
        with TemporaryDirectory() as tmp:
            create_fixture = CreateCompanyFixture(sample_size=10, parent_dir=tmp)

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
