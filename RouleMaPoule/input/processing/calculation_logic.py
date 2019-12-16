from input.models import Waypoint, Acceleration
from output.models import RoadGrade, TrustRate
from input.errors import notEnoughDataPointsError
import statistics as stat
from datetime import datetime as dt
import logging
logger = logging.getLogger(__name__)

def calculate_road_grade(waypoint_latitude, waypoint_longitude):
    """
    Function that performs the calculation for the state of the road.
    Calculation is made on the relative acceleration data.
    """
    accel_data = []
    waypoint_id_list = []

    #retrieve all waypoint objects related to given latitude and longitude
    waypoint_queryset = Waypoint.objects.filter(latitude = waypoint_latitude, longitude = waypoint_longitude)
    for waypoint_item in waypoint_queryset.iterator():
        waypoint_id_list.append(waypoint_item.id)

    #retrieve acceleration data relative to all waypoint objects
    accel_queryset = Acceleration.objects.filter(waypoint_id__in = waypoint_id_list)
    for accel_item in accel_queryset.iterator(): #use of iterator to avoid loading all queryset results in cache. Can cause performance issue.
        accel_data.append(accel_item.accelz)
        
    if len(accel_data) < 15:
        #not enough data points for statistics calculation. Raise custom error.
        raise notEnoughDataPointsError
    else:
        mu = stat.mean(accel_data)
        stdev = stat.stdev(accel_data)
        if mu == 0: 
            raise ZeroDivisionError
        else:
            coeff_var = stdev / mu
            road_grade = (1 - coeff_var) * 5
            return float(road_grade)

def calculate_trust_rate(waypoint_latitude, waypoint_longitude):
    """
    Function that performs the calculation of the trust rate indicator.
    Calculation is based on relative road grades.
    """
    road_grade_data = []       
    road_grade_queryset = RoadGrade.objects.filter(latitude = waypoint_latitude, longitude = waypoint_longitude)
    for road_grade_item in road_grade_queryset.iterator(): #use of iterator to avoid loading all queryset results in cache. Can cause performance issue.
        road_grade_data.append(road_grade_item.grade)
        
    if len(road_grade_data) < 5:
        raise notEnoughDataPointsError
    else:
        mu = stat.mean(road_grade_data)
        stdev = stat.stdev(road_grade_data)
        if mu == 0:
            raise ZeroDivisionError
        else:
            coeff_var = stdev / mu
            trust_rate = 1 - coeff_var
            return float(trust_rate)

def calculation_needed(waypoint_latitude, waypoint_longitude):
    """
    Function that will return true if a new calculation process is needed for a given latitude and longitude, 
    and false if calculations are up to date
    """
    #check if waypoint has related roadgrade data
    related_grades_queryset = RoadGrade.objects.filter(latitude = waypoint_latitude, longitude = waypoint_longitude)
    if not related_grades_queryset:
        #no roadgrade data, calculation process needs to be run
        return True
    else: 
        #check last roadgrade calculation time
        last_grade_calc = related_grades_queryset.latest('timestamp')
        last_grade_calc_time = last_grade_calc.timestamp
        #retrieve waypoint ids for the given latitude and longitude
        waypoint_list = []
        waypoint_queryset = Waypoint.objects.filter(latitude = waypoint_latitude, longitude = waypoint_longitude)
        for waypoint_item in waypoint_queryset.iterator():
            waypoint_list.append(waypoint_item.id)
            
        #check if new acceleration data is available for waypoint
        new_acceleration_data = Acceleration.objects.filter(waypoint_id__in = waypoint_list,timestamp__gt = last_grade_calc_time)
        if not new_acceleration_data:
            #no new acceleration data was found
            return False
        else:
            return True

def process_calculation():
    """
    Function that will perform the calculation of road_grade and trust_rate for all distinct latitude and longitude
    """
    try:
        #get all the distinct longitude and latitude values
        distinct_queryset = Waypoint.objects.values('latitude','longitude').distinct()
        for item in distinct_queryset.iterator():
            #check if calculation is needed for given latitude and longitude data
            if calculation_needed(item.latitude, item.longitude):
                #perform new data calculation
                road_grade = calculate_road_grade(item.latitude, item.longitude)
                trust_rate = calculate_trust_rate(item.latitude, item.longitude)
                #save new data to database
                new_roadgrade = RoadGrade.objects.create(timestamp = dt.now(), grade = road_grade, longitude = item.longitude, latitude = item.latitude)
                new_trustrate = TrustRate.objects.create(timestamp = dt.now(), rate = trust_rate, longitude = item.longitude, latitude = item.latitude)

    except ZeroDivisionError:
        logger.warning("Calculation error for latitude " + item.latitude + " and longitude " + item.longitude + " : unable to process data if mean equals 0")
    
    except notEnoughDataPointsError:
        logger.warning("Calculation error for latitude " + item.latitude + " and longitude " + item.longitude + " : more data points are need for calculation")