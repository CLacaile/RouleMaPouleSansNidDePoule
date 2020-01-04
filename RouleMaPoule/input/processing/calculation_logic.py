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
    
    #print("Related grades for [" + str(waypoint_longitude) + "," + str(waypoint_latitude) + "] : " + str(road_grade_data))
        
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

def grade_calculation_needed(waypoint_latitude, waypoint_longitude):
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
            #print("Reference Time : " + str(last_grade_calc_time))
            return False
        else:
            return True

    
def trustrate_calculation_needed(waypoint_latitude, waypoint_longitude):
    """
    Functions that will return true if a new trustrate calculation is needed for given latitude and longitude,
    and false if calculations are up to date
    """
    #check if waypoint has related trust rate data
    related_trust_queryset = TrustRate.objects.filter(latitude = waypoint_latitude, longitude = waypoint_longitude)
    
    if not related_trust_queryset:
        #no trust rate data, calculation needs to be run
        return True
    else:
        #check last trust rate calculation time
        last_trust_calc = related_trust_queryset.latest('timestamp')
        last_trust_calc_time = last_trust_calc.timestamp
        #check if new road grade is available for waypoint
        new_roadgrade_data = RoadGrade.objects.filter(latitude = waypoint_latitude, longitude = waypoint_longitude, timestamp__gt = last_trust_calc_time)
        if not new_roadgrade_data:
            #no new roadgrade was found
            return False
        else:
            return True

def process_road_grade_calc():
    """
    Function that performs road grade calculation if needed
    """
    try:
        waypoint_list = []
        distinct_waypoints_list = []
        #get all the waypoints objects
        waypoint_queryset = Waypoint.objects.all()
        for item in waypoint_queryset.iterator():
            #create sublist with location data
            waypoint_list.append([item.longitude, item.latitude])
        #keep only distinct values inside list
        for x in waypoint_list:
            if x not in distinct_waypoints_list:
                distinct_waypoints_list.append(x)
        
        for i in range(len(distinct_waypoints_list)):
            #check if calculation is needed for location data
            item_longitude = float(distinct_waypoints_list[i][0])
            item_latitude = float(distinct_waypoints_list[i][1])
            if grade_calculation_needed(item_latitude, item_longitude):
                #perform new data calculation
                try:
                    road_grade = calculate_road_grade(item_latitude, item_longitude)
                
                except ZeroDivisionError:
                    logger.warning("Road Grade calculation error for latitude " + str(item_latitude) + " and longitude " + str(item_longitude) + " : unable to process data if mean equals 0")

                except notEnoughDataPointsError:
                    logger.warning("Road Grade calculation error for latitude " + str(item_latitude) + " and longitude " + str(item_longitude) + " : more data points are needed for calculation")
                
                else:
                    #save road grade data to database
                    new_roadgrade = RoadGrade.objects.create(timestamp = dt.now(), grade = road_grade, longitude = item_longitude, latitude = item_latitude)
                    print("Roadgrade has been successfully added for long : " + str(item_longitude) + " and lat : " + str(item_latitude) + ". Result = " + str(road_grade))
            else:
                print("Data calculation not needed for [" + str(item_longitude) + ", " + str(item_latitude) + "]")
    except:
        pass

def process_trust_rate_calc():
    """
    Function that performs trust rate calculation if needed
    """
    try:
        waypoint_list = []
        distinct_waypoints_list = []
        #get all the waypoints objects
        waypoint_queryset = Waypoint.objects.all()
        for item in waypoint_queryset.iterator():
            #create sublist with location data
            waypoint_list.append([item.longitude, item.latitude])
        #keep only distinct values inside list
        for x in waypoint_list:
            if x not in distinct_waypoints_list:
                distinct_waypoints_list.append(x)

        for i in range(len(distinct_waypoints_list)):
            location_longitude = float(distinct_waypoints_list[i][0])
            location_latitude = float(distinct_waypoints_list[i][1])

            if trustrate_calculation_needed(location_latitude, location_longitude):
                try:
                    trust_rate = calculate_trust_rate(location_latitude,location_longitude)
                
                except ZeroDivisionError:
                    logger.warning("Trust Rate calculation error for latitude " + str(location_latitude) + " and longitude " + str(location_longitude) + " : unable to process data if mean equals 0")
                
                except notEnoughDataPointsError:
                    logger.warning("Trust Rate calculation error for latitude " + str(location_latitude) + " and longitude " + str(location_longitude) + " : more data points are needed for calculation")

                else:
                    new_trustrate = TrustRate.objects.create(timestamp = dt.now(), rate = trust_rate, longitude = location_longitude, latitude = location_latitude)
                    print("Trustrate has been successfully added for long : " + str(location_longitude) + " and lat : " + str(location_latitude) + ". Result = " + str(trust_rate))
    except:
        pass