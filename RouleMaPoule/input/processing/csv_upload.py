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


def check_csv(fields):
    print(len(fields))
    if len(fields) < 7 or len(fields) > 7:
        raise WrongNumberOfColumns

    for i in range(len(fields)):
        if i == DATE:
            datetime.strptime(fields[i], '%Y-%m-%d %H:%M:%S')

        if i == ID_SENSOR:
            int(fields[i])

        if i == LATITUDE:
            float(fields[i])
            if float(fields[i]) > 90 or float(fields[i]) < -90:
                raise WrongGPSData

        if i == LONGITUDE:
            float(fields[i])
            if float(fields[i]) > 180 or float(fields[i]) < -180:
                raise WrongGPSData

        if i == ACCELX:
            int(fields[i])
            if int(fields[i]) > 65535 or int(fields[i]) < 0:
                raise WrongAccelerationValue

        if i == ACCELY:
            int(fields[i])
            if int(fields[i]) > 65535 or int(fields[i]) < 0:
                raise WrongAccelerationValue

        if i == ACCELZ:
            int(fields[i])
            if int(fields[i]) > 65535 or int(fields[i]) < 0:
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

        index = 1

        lines = csv_file.split("\n")
        for line in lines:
            if(index>1):
                fields = line.split(",")
                try:
                    check_csv(fields)
                    if (id_sensor == NOT_DEFINED):
                        try:
                            path.id_sensor = int(fields[ID_SENSOR])
                        except:
                            logger.warning("CSV import : row " + str(index) + " INVALID id_sensor")
                    if (fields[LATITUDE] != last_waypoint.latitude or fields[LONGITUDE] != last_waypoint.latitude):
                        waypoint = Waypoint(latitude=float(fields[LATITUDE]), longitude=float(fields[LONGITUDE]))
                        waypoint.save()
                        path.waypoints.add(waypoint)
                    acceleration = Acceleration(timestamp=fields[DATE], accelx=fields[ACCELX], accely=fields[ACCELY],
                                                accelz=fields[ACCELZ])
                    acceleration.save()
                    waypoint.accelerations.add(acceleration)
                    waypoint.save()
                except WrongNumberOfColumns:
                    logger.warning("CSV import : row " + str(index) + " Wrong number of columns")

                except WrongGPSData:
                    logger.warning("CSV import : row " + str(index) + " Wrong GPS data")

                except WrongAccelerationValue:
                    logger.warning("CSV import : row " + str(index) + " The acceleration number is out of bounds")

                except ValueError:
                    tb = traceback.format_exc()
                    logger.warning("CSV import : row " + str(index) + " " + tb.title())

                except Exception as e:
                    logger.warning("CSV import : row " + str(index) + " " + str(e))
            index += 1
        path.save()
