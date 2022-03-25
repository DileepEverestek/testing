class Unauthorized(BaseException):
    pass

class UserInfoException(Exception):
    ...

class ExpiredSignatureError(UserInfoException):
    def __init__(self):
        self.status_code = 401
        self.detail = "Token expired exception"

class Unauthorized(UserInfoException):
    def __init__(self):
        self.status_code = 401
        self.detail = "Email address doesn't exist in our system."


class BadRequest(UserInfoException):
    def __init__(self):
        self.status_code = 400
        self.detail = "Bad Request"


class UserInfoNotFoundError(UserInfoException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Please enter email address."


class UserInfoInfoAlreadyExistError(UserInfoException):
    def __init__(self):
        self.status_code = 409
        self.detail = "email is already being used"
