class APIException(Exception):
    def __init__(self, status_code: int, message: str, *args):
        self.status_code = status_code
        self.message = message
        super().__init__(*args)


class NotFoundError(APIException):
    def __init__(self, message: str = "Resource not found", *args):
        super().__init__(404, message, *args)
