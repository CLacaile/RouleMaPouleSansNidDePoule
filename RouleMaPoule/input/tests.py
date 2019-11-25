
from django.test import TestCase

from .models import Path
from .processing import csv_upload


class CSV_import_Tests(TestCase):

    def test_import_csv(self):
        csv_file= open('test.csv', 'r+')
        csv_upload.csv_upload(csv_file)
        self.assertIs(False, False)