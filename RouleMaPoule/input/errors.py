from input.exceptions import Error

class WrongNumberOfColumns(Error):
    pass


class WrongAccelerationValue(Error):
    pass

class WrongGPSData(Error):
    pass

class notEnoughDataPointsError(Error):
    pass