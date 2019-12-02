
from django.test import TestCase
from random import seed
from random import randint
from datetime import datetime as dt

from .models import Path, Waypoint, Acceleration
from .processing import csv_upload, calculation_logic

class CSV_import_Tests(TestCase):

    def test_import_csv(self):
        csv_file= open('test.csv', 'r+')
        csv_upload.csv_upload(csv_file.read())
        self.assertIs(False, False)

class calc_logic_tests(TestCase):

    def test_calc_processing(self):
        #create test data
        path_test = Path(id = 1, id_sensor = 0)
        path_test.save()
        waypoint_test = Waypoint(id = 1, longitude = float(47.3901), latitude = float(0.6869))
        waypoint_test.path_id = path_test.id
        waypoint_test.save()

        seed(1)
        
        for i in range(20):
            accel_value = randint(0, 65535)
            accel_test = Acceleration(id = i, timestamp = dt.now(), accelx = 0, accely = 0, accelz = accel_value)
            accel_test.waypoint_id = waypoint_test.id
            accel_test.save()


        waypoint_testlist = Waypoint.objects.get(id = 1)
        calculation_logic.process_waypoint_calculations(waypoint_testlist)
        self.assertIs(False, False)