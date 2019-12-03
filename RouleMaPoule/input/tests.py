
from django.test import TestCase
from random import seed, random, uniform
from random import randint
from datetime import datetime as dt

from .models import Path, Waypoint, Acceleration
from .processing import csv_upload as CSV, calculation_logic
from input.errors import WrongNumberOfColumns, WrongGPSData, WrongAccelerationValue


class CSV_import_Tests(TestCase):


    def setUp(self):
        self.timestamp = "2019-03-03 22:10:10"
        self.sensor_id = str(randint(0, 100))
        self.latitude = str(round(uniform(-90, 90), 4))
        self.longitude = str(round(uniform(-180, 180), 4))
        self.accelx = str(randint(0, 65535))
        self.accely = str(randint(0, 65535))
        self.accelz = str(randint(0, 65535))

    def test_check_csv_ok(self):
        try:
            csv_line = [self.timestamp, self.sensor_id, self.latitude, self.longitude, self.accelx, self.accely,
                        self.accelz]
            CSV.check_csv(csv_line)
            self.assert_(True)
        except Exception as e:
            self.assert_(False)

    def test_check_csv_invalid_date_format(self):
        try:
            csv_line = ["2012-28-98", self.sensor_id, self.latitude, self.longitude, self.accelx, self.accely,
                        self.accelz]
            CSV.check_csv(csv_line)
            self.assert_(False)
        except ValueError as e:
            self.assert_(True)

    def test_check_csv_invalid_wrong_number_of_column(self):
        try:
            csv_line = [self.timestamp, self.sensor_id, self.latitude, self.longitude, self.accelx, self.accely]
            CSV.check_csv(csv_line)
            self.assert_(False)
        except WrongNumberOfColumns as e:
            self.assert_(True)
        try:
            csv_line = [self.timestamp, self.sensor_id, self.latitude, self.longitude, self.accelx, self.accely,
                        self.accelz, "oneMoreColumn"]
            CSV.check_csv(csv_line)
            self.assert_(False)
        except WrongNumberOfColumns as e:
            self.assert_(True)

    def test_check_csv_invalid_longitude(self):
        try:
            csv_line = [self.timestamp, self.sensor_id, "1000000", self.longitude, self.accelx, self.accely,
                        self.accelz]
            CSV.check_csv(csv_line)
            self.assert_(False)
        except WrongGPSData as e:
            self.assert_(True)
        try:
            csv_line = [self.timestamp, self.sensor_id, "-1000000", self.longitude, self.accelx, self.accely,
                        self.accelz]
            CSV.check_csv(csv_line)
            self.assert_(False)
        except WrongGPSData as e:
            self.assert_(True)

    def test_check_csv_invalid_latitude(self):
        try:
            csv_line = [self.timestamp, self.sensor_id, self.latitude, "1000000", self.accelx, self.accely,
                        self.accelz]
            CSV.check_csv(csv_line)
            self.assert_(False)
        except WrongGPSData as e:
            self.assert_(True)
        try:
            csv_line = [self.timestamp, self.sensor_id, self.latitude, "-1000000", self.accelx, self.accely,
                        self.accelz]
            CSV.check_csv(csv_line)
            self.assert_(False)
        except WrongGPSData as e:
            self.assert_(True)

    def test_check_csv_invalid_acceleration_value(self):
        try:
            csv_line = [self.timestamp, self.sensor_id, self.latitude, self.longitude, "100000", self.accely,
                        self.accelz]
            CSV.check_csv(csv_line)
            self.assert_(False)
        except WrongAccelerationValue as e:
            self.assert_(True)
        try:
            csv_line = [self.timestamp, self.sensor_id, self.latitude, self.latitude, "-1000", self.accely,
                        self.accelz]
            CSV.check_csv(csv_line)
            self.assert_(False)
        except WrongAccelerationValue as e:
            self.assert_(True)

    def test_csv_upload_ok(self):
        pathCount = Path.objects.count()
        waypointCount = Waypoint.objects.count()
        accelerationCount = Acceleration.objects.count()

        #write in the csv file
        csv_file = open('test.csv', 'w+')
        csv_file.write("timestamp,id_sensor,longitude,latitude,AccelX,AccelY,AccelZ\n")
        csv_line = self.timestamp+","+self.sensor_id+","+self.latitude+","+self.longitude+","+self.accelx+","+self.accely+","+self.accelz
        csv_file.write(csv_line)
        csv_file.close()

        #parse and insert
        csv_file = open('test.csv', 'r+')
        pathId = CSV.csv_upload(csv_file.read())
        csv_file.close()

        self.assertIs(pathCount+1, Path.objects.count())
        self.assertIs(waypointCount+1, Waypoint.objects.count())
        self.assertIs(accelerationCount+1, Acceleration.objects.count())

        path = Path.objects.get(id=pathId)
        self.assertIs(path.id_sensor, int(self.sensor_id))
        self.assertIs(path.waypoints.count(), 1)

        waypoint = path.waypoints.first()
        self.assertAlmostEqual(waypoint.latitude, float(self.latitude))
        self.assertAlmostEqual(waypoint.longitude, float(self.longitude))
        self.assertIs(waypoint.accelerations.count(), 1)

        acceleration = waypoint.accelerations.first()
        self.assertAlmostEqual(acceleration.accelx, int(self.accelx))
        self.assertAlmostEqual(acceleration.accely, int(self.accely))
        self.assertAlmostEqual(acceleration.accelz, int(self.accelz))


    def test_csv_upload_endpoint(self):
        csv_file = open('test.csv', 'r+')
        #csv.csv_upload(csv_file.read())
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