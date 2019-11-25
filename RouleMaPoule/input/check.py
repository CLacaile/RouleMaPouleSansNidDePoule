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


def check_csv(row = "2019-09-22 17:34:50, 1, 47.365112, 0.685142, 65529, 3, 29"):
    try:

        data = row.split(", ")

        if len(data) < 7 or len(data) > 7:
            raise WrongNumberOfColumns

        for i in range(len(data)):
            if i == 0:
                datetime.strptime(data[i], '%Y-%m-%d %H:%M:%S')

            if i == 1:
                int(data[i])

            if i == 2:
                float(data[i])
                if float(data[i]) > 90 or float(data[i]) < -90:
                    raise WrongGPSData

            if i == 3:
                float(data[i])
                if float(data[i]) > 180 or float(data[i]) < -180:
                    raise WrongGPSData

            if i == 4:
                int(data[i])
                if int(data[i]) > 65535 or int(data[i]) < 0:
                    raise WrongAccelerationValue

            if i == 5:
                int(data[i])
                if int(data[i]) > 65535 or int(data[i]) < 0:
                    raise WrongAccelerationValue

            if i == 6:
                int(data[i])
                if int(data[i]) > 65535 or int(data[i]) < 0:
                    raise WrongAccelerationValue

    except WrongNumberOfColumns:
        print("Wrong number of columns")

    except WrongGPSData:
        print("Wrong GPS data")

    except WrongAccelerationValue:
        print("The acceleration number is out of bounds")

    except ValueError:
        tb = traceback.format_exc()
        print(tb.title())


if __name__ == "__main__":
    check_csv()



