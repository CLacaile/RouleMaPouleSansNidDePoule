import csv
import logging
import traceback
from datetime import datetime
from input.models import Path, Waypoint, Acceleration
from RouleMaPoule.input.errors import WrongNumberOfColumns, WrongGPSData, WrongAccelerationValue

# CONSTANTS
DATE = 0
ID_SENSOR = 1
LATITUDE = 2
LONGITUDE = 3
ACCELX = 4
ACCELY = 5
ACCELZ = 6
NOT_DEFINED = -666

# Logger
logger = logging.getLogger(__name__)


def check_csv(data):
    """
    Function that checks whether a row of CSV is conform or not. It checks :
    - If the CSV has more or less than 7 columns
    - Parses the date to a datetime
    - Casts the sensor ID to an int
    - Checks whether the latitude given is between 90 and -90
    - Checks whether the longitude is between 180 and -180
    - Checks whether accelx, accely and accelz is between 0 and 65535

    Args:
        - data a row of a CSV file
    
    Raises:
        - WrongNumberOfColumns
        - WrongGPSData
        - WrongAccelerationValue
    """
    if len(data) < 7 or len(data) > 7:
        raise WrongNumberOfColumns

    for i in range(len(data)):
        if i == DATE:
            datetime.strptime(data[i], '%Y-%m-%d %H:%M:%S')

        if i == ID_SENSOR:
            int(data[i])

        if i == LATITUDE:
            float(data[i])
            if float(data[i]) > 90 or float(data[i]) < -90:
                raise WrongGPSData

        if i == LONGITUDE:
            float(data[i])
            if float(data[i]) > 180 or float(data[i]) < -180:
                raise WrongGPSData

        if i == ACCELX:
            int(data[i])
            if int(data[i]) > 65535 or int(data[i]) < 0:
                raise WrongAccelerationValue

        if i == ACCELY:
            int(data[i])
            if int(data[i]) > 65535 or int(data[i]) < 0:
                raise WrongAccelerationValue

        if i == ACCELZ:
            int(data[i])
            if int(data[i]) > 65535 or int(data[i]) < 0:
                raise WrongAccelerationValue

def csv_upload(csv_file):
    """ 
    This function uploades parses a given CSV file into objects and 
    store them in the db, after having checked the file using check_csv.
    
    Args:
        - csv_file a CSV file to insert into the db
    """
    #Check if file is CSV
    #Check if file is empty

    #init Path
    id_sensor = NOT_DEFINED
    last_waypoint = Waypoint()
    waypoint = Waypoint()
    path = Path()
    path.save()

    #read the CSV file
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader, None)  # skip the headers
    index = 1
    for row in csv_reader:
        try:
            check_csv(row)
            if(id_sensor==NOT_DEFINED):
                try:
                        path.id_sensor = int(row[ID_SENSOR])
                except:
                    logger.warning("CSV import : row "+str(index)+" INVALID id_sensor")
            if(row[LATITUDE]!=last_waypoint.latitude or row[LONGITUDE]!=last_waypoint.latitude):
                waypoint = Waypoint(latitude=float(row[LATITUDE]),longitude=float(row[LONGITUDE]))
                waypoint.save()
                path.waypoints.add(waypoint)
            acceleration =  Acceleration(timestamp=row[DATE], accelx=row[ACCELX], accely=row[ACCELY], accelz=row[ACCELZ])
            acceleration.save()
            waypoint.accelerations.add(acceleration)
            waypoint.save()
        except WrongNumberOfColumns:
            logger.warning("CSV import : row "+str(index)+"Wrong number of columns")

        except WrongGPSData:
            logger.warning("CSV import : row "+str(index)+"Wrong GPS data")

        except WrongAccelerationValue:
            logger.warning("CSV import : row "+str(index)+" The acceleration number is out of bounds")

        except ValueError:
            tb = traceback.format_exc()
            logger.warning("CSV import : row "+str(index)+" "+tb.title())

        except Exception as e:
            logger.warning("CSV import : row "+str(index)+" "+str(e))
        index += 1
    path.save()
