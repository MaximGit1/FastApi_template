from fastapi import HTTPException, status

USER_ALREADY_EXISTS = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="A user with that name already exists",
)

USER_NOT_EXISTS = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="The user is unauthorized",
)

USER_DO_NOT_HAS_THIS_PERMISSION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="The user has not this permissions!",
)
