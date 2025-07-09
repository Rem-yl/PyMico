from typing import List, Optional

from database import Base
from log import logger
from models.data.signup import Member, SignUp, Trainer
from sqlalchemy.orm import Session


class SignUpRepo:
    _init = True

    def __init__(self, sess: Session) -> None:
        self.sess = sess
        if self._init:
            Base.metadata.create_all(self.sess.bind)
            self._init = False

    def add(self, model: SignUp) -> Optional[SignUp]:
        try:
            exist_signup = (
                self.sess.query(SignUp).filter_by(username=model.username).first()
            )
            if exist_signup:
                logger.warning(
                    f"SignUp failed: username '{model.username}' already exists."
                )
                return exist_signup

            self.sess.add(model)
            self.sess.commit()
            logger.info(f"SignUp successful for user: {model.username}")
            return model

        except Exception as e:
            self.sess.rollback()
            logger.error(f"Error during SignUp for user {model.username}: {e}")
            return None

    def update(self, model: SignUp, new_model: SignUp) -> Optional[SignUp]:
        try:
            exist_signup = (
                self.sess.query(SignUp).filter_by(username=model.username).first()
            )

            if exist_signup is None:
                logger.warning(
                    f"Update failed: username '{model.username}' does not exist."
                )
                return None

            if model.password != exist_signup.password:
                logger.warning(
                    f"Update failed: invalid password for username '{model.username}'."
                )
                return None

            exist_signup.username = new_model.username
            exist_signup.password = new_model.password
            exist_signup.user_type = new_model.user_type
            self.sess.commit()
            logger.info(f"Update successful for user: {model.username}")
            return new_model

        except Exception as e:
            self.sess.rollback()
            logger.error(f"Error during Update for user {model.username}: {e}")
            return None

    def delete(self, username: str, password: str) -> bool:
        try:
            signup = self.sess.query(SignUp).filter_by(username=username).first()
            if signup is None:
                logger.warning(f"Delete failed: username '{username}' does not exist.")
                return False

            if signup.password != password:
                logger.warning(
                    f"Delete failed: invalid password for username '{username}'."
                )
                return False

            self.sess.delete(signup)
            self.sess.commit()
            logger.info(f"Delete successful for user: {username}")
            return True

        except Exception as e:
            self.sess.rollback()
            logger.error(f"Error during Delete for user {username}: {e}")
            return False

    def list_signups(self) -> List[SignUp]:
        try:
            signups: List[SignUp] = self.sess.query(SignUp).all()
            return signups
        except Exception as e:
            logger.error(f"Error during list_signups: {e}")
            return []


class MemberSignupRepo:
    def __init__(self, sess: Session) -> None:
        self.sess = sess

    def add(self, model: Member) -> Optional[Member]:
        try:
            exist_member = (
                self.sess.query(Member).filter_by(signup_id=model.signup_id).first()
            )
            if exist_member:
                logger.warning(
                    f"MemberSignUp failed: username '{exist_member.signup.username}' already exists."
                )
                return exist_member

            self.sess.add(model)
            self.sess.commit()
            self.sess.refresh(model)
            logger.info(f"MemberSignUp successful for user: {model.signup.username}")
            return model

        except Exception as e:
            self.sess.rollback()
            logger.error(
                f"Error during MemberSignUp for user signup id {model.signup_id}: {e}"
            )
            return None

    def list_members(self) -> List[Member]:
        try:
            members: List[Member] = self.sess.query(Member).join(Member.signup).all()
            return members

        except Exception as e:
            logger.error(f"Error during list_members: {e}")
            return []


class TrainerSignupRepo:
    def __init__(self, sess: Session) -> None:
        self.sess = sess

    def add(self, model: Trainer) -> Optional[Trainer]:
        try:
            exist_trainer = (
                self.sess.query(Trainer).filter_by(signup_id=model.signup_id).first()
            )
            if exist_trainer:
                logger.warning(
                    f"TrainerSignUp failed: username '{exist_trainer.signup.username}' already exists."
                )
                return exist_trainer

            self.sess.add(model)
            self.sess.commit()
            self.sess.refresh(model)
            logger.info(f"TrainerSignUp successful for user: {model.signup.username}")
            return model

        except Exception as e:
            self.sess.rollback()
            logger.error(
                f"Error during TrainerSignUp for user signup id {model.signup_id}: {e}"
            )
            return None

    def list_trainers(self) -> List[Trainer]:
        try:
            trainers: List[Trainer] = self.sess.query(Trainer).all()
            return trainers
        except Exception as e:
            logger.error(f"Error during list_trainers: {e}")
            return []
