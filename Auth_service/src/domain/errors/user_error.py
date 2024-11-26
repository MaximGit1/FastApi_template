from fastapi import HTTPException, status

USER_ALREADY_EXISTS = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="A user with that name already exists",
)
