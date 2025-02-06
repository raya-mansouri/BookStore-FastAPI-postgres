from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import HTTPException, status
from app.models.user import User  
from app.schemas.user import UserCreate, UserUpdate, UserOut  
from .utils import hash_password, verify_password  

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate) -> UserOut:
        """
        Create a new user with a hashed password.
        """
        try:
            # Hash the password before saving it
            hashed_password = hash_password(user.password)
            db_user = User(**user.model_dump(exclude={"password"}), password=hashed_password)
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return UserOut.model_validate(db_user)
        except IntegrityError as e:
            self.db.rollback()
            if "username" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already exists.",
                )
            elif "email" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists.",
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An error occurred while creating the user.",
                )

    def get_user_by_id(self, user_id: int) -> UserOut:
        """
        Retrieve a user by ID.
        """
        try:
            db_user = self.db.query(User).filter(User.id == user_id).one()
            return UserOut.model_validate(db_user)
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

    def get_all_users(self) -> list[UserOut]:
        """
        Retrieve all users from the database.
        """
        try:
            db_users = self.db.query(User).all()
            return [UserOut.model_validate(db_user) for db_user in db_users]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while retrieving users: {str(e)}",
            )
        
    def update_user(self, user_id: int, user: UserUpdate) -> UserOut:
        """
        Update a user by ID.
        """
        try:
            db_user = self.db.query(User).filter(User.id == user_id).one()
            update_data = user.model_dump(exclude_unset=True)
            if "password" in update_data:
                # Hash the new password before updating
                update_data["password"] = hash_password(update_data["password"])
            for key, value in update_data.items():
                setattr(db_user, key, value)
            self.db.commit()
            self.db.refresh(db_user)
            return UserOut.model_validate(db_user)
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )
        except IntegrityError as e:
            self.db.rollback()
            if "username" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already exists.",
                )
            elif "email" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists.",
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An error occurred while updating the user.",
                )

    def delete_user(self, user_id: int) -> None:
        """
        Delete a user by ID.
        """
        try:
            db_user = self.db.query(User).filter(User.id == user_id).one()
            self.db.delete(db_user)
            self.db.commit()
        except NoResultFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )
        return {"message": "User deleted successfully", "user_id": user_id}
