from fastapi import HTTPException, status

class UserServiceException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class UserNotFound(UserServiceException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

class UserAlreadyExists(UserServiceException):
    def __init__(self, field: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{field.capitalize()} already exists.")

class InternalServerError(UserServiceException):
    def __init__(self, detail: str = "An error occurred while processing the request."):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)