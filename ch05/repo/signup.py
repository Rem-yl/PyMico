from typing import List

from log import logger
from models.login import Signup
from sqlalchemy.orm import Session


class SignupRepository:
    def __init__(self, sess: Session) -> None:
        self.sess = sess

    def insert_signup(self, signup: Signup) -> bool:
        try:
            # 重复性检查（是否已有相同 username）
            existing = (
                self.sess.query(Signup).filter_by(username=signup.username).first()
            )
            if existing:
                logger.warning(
                    f"Signup failed: username '{signup.username}' already exists."
                )
                return True

            # 插入数据
            self.sess.add(signup)
            self.sess.commit()
            logger.info(f"Signup successful for user: {signup.username}")
            return True

        except Exception as e:
            self.sess.rollback()
            logger.error(f"Error during signup for user {signup.username}: {e}")
            return False

    def update_signup(self, id: int, new_signup: Signup) -> bool:
        try:
            existing_signup = self.sess.query(Signup).filter(Signup.id == id).first()
            if not existing_signup:
                logger.warning(f"Signup with id {id} not found for update.")
                return False

            existing_signup.username = new_signup.username
            existing_signup.password = new_signup.password
            self.sess.commit()
            logger.info(
                f"Signup updated successfully for user: {existing_signup.username}"
            )
        except Exception as e:
            self.sess.rollback()
            logger.error(f"Error updating signup for user {new_signup.username}: {e}")
            return False

        return True

    def delete_signup(self, id: int) -> bool:
        try:
            existing_signup = self.sess.query(Signup).filter(Signup.id == id).first()
            if not existing_signup:
                logger.warning(f"Signup with id {id} not found for deletion.")
                return False

            self.sess.delete(existing_signup)
            self.sess.commit()
            logger.info(
                f"Signup deleted successfully for user: {existing_signup.username}"
            )
        except Exception as e:
            self.sess.rollback()
            logger.error(f"Error deleting signup with id {id}: {e}")
            return False

        return True

    def get_all(self) -> List[Signup]:
        try:
            signups: List[Signup] = self.sess.query(Signup).all()
            logger.info(f"Retrieved {len(signups)} signups.")
            return signups
        except Exception as e:
            logger.error(f"Error retrieving signups: {e}")
            return []
