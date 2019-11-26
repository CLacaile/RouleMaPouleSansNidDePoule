
from django.test import TestCase

from .models import Path, Waypoint
from .processing import csv_upload, calculation_logic

"""
class CSV_import_Tests(TestCase):

    def test_import_csv(self):
        csv_file= open('test.csv', 'r+')
        csv_upload.csv_upload(csv_file)
        self.assertIs(False, False)

class calc_logic_tests(TestCase):

    def test_calc_processing(self):
        waypoint_test = Waypoint.objects.get(id = 1)
        calculation_logic.process_waypoint_calculations(waypoint_test)
        self.assertIs(False, False)
"""