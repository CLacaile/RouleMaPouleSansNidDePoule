import csv
import logging
logger = logging.getLogger(__name__)

from input.models import Path, Waypoint, Acceleration

DATE = 0
ID_SENSOR = 1
LATITUDE = 2
LONGITUDE = 3
ACCELX = 4
ACCELY = 5
ACCELZ = 6

NOT_DEFINED = -666

import traceback
from datetime import datetime


class Error(Exception):
    pass


class WrongNumberOfColumns(Error):
    pass


class WrongAccelerationValue(Error):
    pass


class WrongGPSData(Error):
    pass


def check_csv(data ):
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
