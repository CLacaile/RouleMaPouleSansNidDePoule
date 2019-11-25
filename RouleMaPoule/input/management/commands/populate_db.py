from django.core.management.base import BaseCommand
from input.models import Path, Acceleration, Waypoint
import datetime
import random

#47.3901, 0.6873
class Command(BaseCommand):
    #args = '<foo bar ...>'
    #help = 'our help string comes here'

    def populate(self):
        random.seed(666)
        for pathIndex in range(4):
            path = Path(id_sensor=pathIndex)
            path.save()
            for i in range(5):
              #  0.6869, 0.6875, 0.0001
                lattitude = float("{0:.4f}".format(0.6869+(0.0001*i)))
                waypoint = Waypoint(longitude=47.3901, latitude=lattitude)
                waypoint.save()
                path.waypoints.add(waypoint)
                for y in range(36):
                    startDate = datetime.datetime.now()
                    date = startDate + datetime.timedelta(milliseconds=200*y)
                    accelx = random.randint(0,65535)
                    acceleration = Acceleration(timestamp=date, accelx=accelx, accely=0, accelz=0)
                    acceleration.save()
                    waypoint.accelerations.add(acceleration)
            path.save()

    def handle(self, *args, **options):
        self.populate()