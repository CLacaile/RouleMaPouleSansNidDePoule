from input.models import Waypoint, Acceleration
from output.models import RoadGrade, TrustRate
from input.errors import notEnoughDataPointsError
import statistics as stat
from datetime import datetime as dt
import logging
logger = logging.getLogger(__name__)

def calculate_road_grade(waypointObject):
    """
    Function that performs the calculation for the state of the road.
    Calculation is made on the relative acceleration data.
    """
    try:
        accel_data = []
        accel_queryset = Acceleration.objects.filter(waypoint_id = waypointObject.id)
        for accel_item in accel_queryset.iterator(): #use of iterator to avoid loading all queryset results in cache. Can cause performance issue.
            accel_data.append(accel_item.accelz)
        
        if len(accel_data) < 15:
            #not enough data points for statistics calculation. Raise custom error.
            raise notEnoughDataPoints
        else:
            mu = stat.mean(accel_data)
            stdev = stat.stdev(accel_data)
            if mu == 0: 
                raise ZeroDivisionError
            else:
                coeff_var = stdev / mu
                road_grade = (1 - coeff_var) * 5
                return road_grade
    except:
        pass

def calculate_trust_rate(waypointObject):
    """
    Function that performs the calculation of the trust rate indicator.
    Calculation is based on relative road grades.
    """
    try:
        road_grade_data = []
        road_grade_queryset = RoadGrade.objects.filter(road_waypoint_id = waypointObject.id)
        for road_grade_item in road_grade_queryset.iterator(): #use of iterator to avoid loading all queryset results in cache. Can cause performance issue.
            road_grade_data.append(road_grade_item.grade)
        
        if len(road_grade_data) < 5:
            raise notEnoughDataPoints
        else:
            mu = stat.mean(road_grade_data)
            stdev = stat.stdev(road_grade_data)
            if mu == 0:
                raise ZeroDivisionError
            else:
                coeff_var = stdev / mu
                trust_rate = 1 - coeff_var
                return float(trust_rate)
    except:
        pass

def process_waypoint_calculations(waypointObject):
    """
    Procedure that make the road grade and trust rate calculations and save 
    RoadGrade and TrustRate objects to database
    """
    new_roadgrade = RoadGrade()
    new_trustrate = TrustRate()

    try:
        road_grade = calculate_road_grade(waypointObject)
        trust_rate = calculate_trust_rate(waypointObject)

        new_roadgrade = RoadGrade(timestamp = dt.now(), grade = float(road_grade))
        new_roadgrade.road_waypoint_id = waypointObject.id
        new_roadgrade.save()

        new_trustrate = TrustRate(timestamp = dt.now(), rate = trust_rate)
        new_trustrate.trust_waypoint_id = waypointObject.id
        new_trustrate.save()
    
    except ZeroDivisionError:
        logger.warning("Calculation error for waypoint " + waypointObject.id + " : unable to process data if mean equals 0")
    
    except notEnoughDataPointsError:
        logger.warning("Calculation error for waypoint " + waypointObject.id + " : more data points are need for calculation") 