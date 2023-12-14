class RobotException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        raise NotImplementedError


class DriverVersionException(RobotException):
    def __init__(self, message: str = 'Chrome version is incompatible with webdriver version, please open chrome and '
                                      'get [chrome://version/] and check webdriver version in setting.py'):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"
