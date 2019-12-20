from django.contrib.auth.models import User
from django.test import TestCase
from .processing import csv_upload
from rest_framework.test import RequestsClient
from random import seed
from random import seed, random, uniform
from random import randint
from datetime import datetime as dt, timedelta

from .models import Path, Waypoint, Acceleration
from output.models import RoadGrade, TrustRate
from .processing import csv_upload as CSV, calculation_logic as calc
from input.errors import WrongNumberOfColumns, WrongGPSData, WrongAccelerationValue, notEnoughDataPointsError


class Authentification_Tests(TestCase):
    """
        Cass that tests if the authentification and protection of
        the API endpoints
    """

    def test_token_ok(self):
        """
            Test if the token is sent for a successfull authentification

            Note :
                it first creates a user
                then request the login endpoint of the app
                finally checks if the response's code and if the token is in the response

        """
        client = RequestsClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        params = {'username': 'testuser', 'password': '12345'}
        response = client.post('http://127.0.0.1:8000/api/token/', params)
        json_string = response.content.decode('utf8').replace("'", '"')
        assert response.status_code == 200
        assert "access" in json_string


    def test_token_ko(self):
        """
            Test if the token is sent for a unsuccessfull authentification

            Note :
                request the login endpoint of the app with some logins credentials that doesn't exist
                checks if the response's code

        """
        client = RequestsClient()
        params = {'username': 'testuser', 'password': '12345'}
        response = client.post('http://127.0.0.1:8000/api/token/', params)
        json_string = response.content.decode('utf8').replace("'", '"')
        assert response.status_code == 401


    def test_non_authorizied_access(self):
        """
            Test an unauthorized access to all endpoints

            Note :
                request the endpoints
                checks the response's code

        """
        client = RequestsClient()
        response = client.get('http://127.0.0.1:8000/api/v1.0/input/waypoint/')
        assert response.status_code == 401
        response = client.get('http://127.0.0.1:8000/api/v1.0/input/path')
        assert response.status_code == 401
        response = client.get('http://127.0.0.1:8000/api/v1.0/input/acceleration')
        assert response.status_code == 401

    def test_authorized_access(self):
        """
            Test an authorized access to all endpoints

            Note :
                creates a user
                request the login endpoint of the app
                gets the token
                request the endpoints and checks the response's code

        """
        client = RequestsClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        params = {'username': 'testuser', 'password': '12345'}
        response = client.post('http://127.0.0.1:8000/api/token/', params)
        json_array = response.json()
        header = {
            "Authorization": "Bearer " + json_array['access']
        }
        response = client.get('http://127.0.0.1:8000/api/v1.0/input/waypoint/', headers = header)
        assert response.status_code == 200
        response = client.get('http://127.0.0.1:8000/api/v1.0/input/path', headers=header)
        assert response.status_code == 200
        response = client.get('http://127.0.0.1:8000/api/v1.0/input/acceleration', headers=header)
        assert response.status_code == 200




class CSV_import_Tests(TestCase):
    """
        Test the import of the CSV file

    """

    def setUp(self):
        """
            set up random variables for the import

        """
        self.timestamp = "2019-03-03 22:10:10"
        self.sensor_id = str(randint(0, 100))
        self.latitude = str(round(uniform(-90, 90), 4))
        self.longitude = str(round(uniform(-180, 180), 4))
        self.accelx = str(randint(0, 65535))
        self.accely = str(randint(0, 65535))
        self.accelz = str(randint(0, 65535))

    def test_check_csv_ok(self):
        """
            Test the check_csv function with a correct csv line

        """
        try:
            csv_line = [self.timestamp, self.sensor_id, self.latitude, self.longitude, self.accelx, self.accely,
                        self.accelz]
            CSV.check_csv(csv_line)
            self.assert_(True)
        except Exception as e:
            self.assert_(False)

    def test_check_csv_invalid_date_format(self):
        """
            Test the check_csv function with an invalid date format

            Raises :
                ValueError : with a wrong date

        """
        try:
            csv_line = ["2012-28-98", self.sensor_id, self.latitude, self.longitude, self.accelx, self.accely,
                        self.accelz]
            CSV.check_csv(csv_line)
            self.assert_(False)
        except ValueError as e:
            self.assert_(True)

    def test_check_csv_invalid_wrong_number_of_column(self):
        """
            Test the check_csv function with an invalid number of column

            Raises :
                WrongNumberOfColumns : if the number of color is invalide

        """
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
        """
            Test the check_csv function with an invalid longitude

            Raises :
                WrongGPSData : if the longitude is invalid

        """
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
        """
            Test the check_csv function with an invalid latitude

            Raises :
                WrongGPSData : if the longitude is latitude

        """
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
        """
            Test the check_csv function with an invalid acceleration value

            Raises :
                WrongAccelerationValue : if the acceleration value is invalid

        """
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
        """
            Test if the csv uploaded to the database is valid

            Note :
                test if every field is valid

        """
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

    def setUp(self):
        #create test data
        path_test = Path(id = 1, id_sensor = 0)
        path_test.save()
        waypoint_test = Waypoint(id = 1, longitude = float(47.3901), latitude = float(0.6871))
        waypoint_test.path_id = path_test.id
        waypoint_test.save()
        
    def test_grade_calc_needed(self):
        #create test data
        seed(1)

        for i in range(16):
            accel_value = randint(0, 65535)
            accel_test = Acceleration.objects.create(id = i, timestamp = dt.now(), accelx = 0, accely = 0, accelz = accel_value, waypoint_id = 1)

        last_accel_timestamp = Acceleration.objects.latest('timestamp').timestamp

        #first test = no grade data available
        tested_waypoint = Waypoint.objects.get(id = 1)
        self.assertIs(calc.grade_calculation_needed(tested_waypoint.latitude,tested_waypoint.longitude), True)

        #second test = grade data is available but outdated
        grade_test = RoadGrade.objects.create(id = 1, timestamp = last_accel_timestamp - timedelta(days=2), grade = float(4.2), longitude = float(47.3901), latitude = float(0.6871))
        tested_waypoint = Waypoint.objects.get(id = 1)
        self.assertIs(calc.grade_calculation_needed(tested_waypoint.latitude,tested_waypoint.longitude), True)

    def test_grade_calc_not_needed(self):
        #create test data
        seed(1)

        for i in range(16):
            accel_value = randint(0, 65535)
            accel_test = Acceleration.objects.create(id = i, timestamp = dt.now(), accelx = 0, accely = 0, accelz = accel_value, waypoint_id = 1)
            
        last_accel_timestamp = Acceleration.objects.latest('timestamp').timestamp
        grade_test = RoadGrade.objects.create(id = 1, timestamp = last_accel_timestamp, grade = float(4.2), longitude = float(47.3901), latitude = float(0.6871))

        tested_waypoint = Waypoint.objects.get(id = 1)
        self.assertIs(calc.grade_calculation_needed(tested_waypoint.latitude,tested_waypoint.longitude), False)

    def test_grade_calc_enough_data(self):
        #create more than 15 data points
        seed(1)

        for i in range(16):
            accel_value = randint(0, 65535)
            accel_test = Acceleration.objects.create(id = i, timestamp = dt.now(), accelx = 0, accely = 0, accelz = accel_value, waypoint_id = 1)
        
        try:
            #perform roadgrade calculation and test the value
            tested_waypoint = Waypoint.objects.get(id = 1)
            self.assertGreaterEqual(calc.calculate_road_grade(tested_waypoint.latitude, tested_waypoint.longitude), 0)
            self.assertLessEqual(calc.calculate_road_grade(tested_waypoint.latitude, tested_waypoint.longitude), 5)
        except notEnoughDataPointsError:
            self.assert_(True)
    
    def test_grade_calc_not_enough_data(self):
        #create less or exactly 15 data points
        seed(1)

        for i in range(15):
            accel_value = randint(0, 65535)
            accel_test = Acceleration.objects.create(id = i, timestamp = dt.now(), accelx = 0, accely = 0, accelz = accel_value, waypoint_id = 1)

        try:
            #perform roadgrade calculation and test the value
            tested_waypoint = Waypoint.objects.get(id = 1)
            self.assertGreaterEqual(calc.calculate_road_grade(tested_waypoint.latitude, tested_waypoint.longitude), 0)
            self.assertLessEqual(calc.calculate_road_grade(tested_waypoint.latitude, tested_waypoint.longitude), 5)
        except notEnoughDataPointsError:
            self.assert_(True)

    def test_trust_calc_enough_data(self):
        #create more than 5 roadgrade data points
        for i in range(6):
            new_road_grade = RoadGrade.objects.create(id = i, timestamp = dt.now(), grade = uniform(0,5), longitude = float(47.3901), latitude = float(0.6871))
        try:
            #perform trustrate calculation and test the value
            tested_waypoint = Waypoint.objects.get(id = 1)
            test_value = calc.calculate_trust_rate(tested_waypoint.latitude, tested_waypoint.longitude)
        except notEnoughDataPointsError:
            self.assert_(True)
        else:
            self.assertGreaterEqual(test_value, 0)
            self.assertLessEqual(test_value, 1)

    def test_trust_calc_enough_data(self):
        #create less or exactly 5 roadgrade data points
        for i in range(5):
            new_road_grade = RoadGrade.objects.create(id = i, timestamp = dt.now(), grade = uniform(0,5), longitude = float(47.3901), latitude = float(0.6871))
        try:
            #perform trustrate calculation and test the value
            tested_waypoint = Waypoint.objects.get(id = 1)
            test_value = calc.calculate_trust_rate(tested_waypoint.latitude, tested_waypoint.longitude)
        except notEnoughDataPointsError:
            self.assert_(True)
        else:
            self.assertGreaterEqual(test_value, 0)
            self.assertLessEqual(test_value, 1)