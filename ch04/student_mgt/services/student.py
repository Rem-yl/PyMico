from typing import Dict

from fastapi import HTTPException
from student_mgt.models.student import Login, Signup, Student, StudentReq

student_signup_repo: Dict[str, Signup] = {}
student_login_repo: Dict[str, Login] = {}
student_repo: Dict[str, Student] = {}


class StudentSignupService:
    def __init__(self) -> None:
        self.repo = student_signup_repo

    def add(self, signup: Signup) -> None:
        uname = signup.username
        if uname in self.repo:
            raise HTTPException(
                status_code=400, detail=f"Username: {uname} already exists"
            )

        self.repo[uname] = signup

    def get(self, username: str) -> Signup:
        if username not in self.repo:
            raise HTTPException(
                status_code=404, detail=f"Username: {username} not found"
            )

        signup = self.repo[username]

        return signup

    def remove(self, username: str) -> None:
        if username not in self.repo:
            raise HTTPException(
                status_code=404, detail=f"Username: {username} not found"
            )

        del self.repo[username]

    def list_all(self) -> Dict[str, Signup]:
        """
        Returns all signups in the repository.

        This method retrieves all signups stored in the repository and returns them as a dictionary.
        The keys are the usernames, and the values are the Signup objects.
        Returns:
            Dict[str, Signup]: A dictionary containing all signups.
        """
        return self.repo.copy()


class StudentLoginService:
    def __init__(self) -> None:
        self.repo = student_login_repo

    def add(self, login: Login) -> None:
        uname = login.username
        if uname in self.repo:
            raise HTTPException(
                status_code=400, detail=f"Username: {uname} already exists"
            )

        self.repo[uname] = login

    def get(self, username: str) -> Login:
        if username not in self.repo:
            raise HTTPException(
                status_code=404, detail=f"Username: {username} not found"
            )

        login = self.repo[username]
        return login

    def remove(self, username: str) -> None:
        if username not in self.repo:
            raise HTTPException(
                status_code=404, detail=f"Username: {username} not found"
            )

        del self.repo[username]

    def update_password(self, username: str, new_password: str) -> None:
        """
        Updates the password for a given username.

        This method updates the password for the specified username in the repository.
        If the username does not exist, it raises an HTTPException with a 404 status code.
        """
        if username not in self.repo:
            raise HTTPException(
                status_code=404, detail=f"Username: {username} not found"
            )

        self.repo[username].password = new_password


class StudentService:
    def __init__(self) -> None:
        self.repo = student_repo

    def add(self, student: Student) -> None:
        if student.name in self.repo:
            raise HTTPException(
                status_code=400,
                detail=f"Student with name: {student.name} already exists",
            )

        self.repo[student.name] = student

    def get(self, name: str) -> Student:
        if name not in self.repo:
            raise HTTPException(
                status_code=404, detail=f"Student with name: {name} not found"
            )

        return self.repo[name]

    def remove(self, name: str) -> None:
        if name not in self.repo:
            raise HTTPException(
                status_code=404, detail=f"Student with name: {name} not found"
            )

        del self.repo[name]

    def list_all(self) -> Dict[str, Student]:
        return self.repo.copy()

    def update(self, new_student: StudentReq) -> None:
        old_student = self.repo.get(new_student.name)
        if not old_student:
            raise HTTPException(
                status_code=404,
                detail=f"Student with name: {new_student.name} not found",
            )

        updated_student = Student(
            id=old_student.id,  # Keep the same ID
            name=new_student.name,
            age=new_student.age,
        )
        self.repo[new_student.name] = updated_student


def get_student_signup_service() -> StudentSignupService:
    """
    Returns an instance of the StudentSignupService.

    This function is used to create and return a new instance of the StudentSignupService class.
    It can be used in dependency injection scenarios where a service instance is required.

    Returns:
        StudentSignupService: An instance of the StudentSignupService class.
    """
    return StudentSignupService()


def get_student_login_service() -> StudentLoginService:
    """
    Returns an instance of the StudentLoginService.

    This function is used to create and return a new instance of the StudentLoginService class.
    It can be used in dependency injection scenarios where a service instance is required.
    Returns:
        StudentLoginService: An instance of the StudentLoginService class.
    """
    return StudentLoginService()


def get_student_service() -> StudentService:
    """
    Returns an instance of the StudentService.

    This function is used to create and return a new instance of the StudentService class.
    It can be used in dependency injection scenarios where a service instance is required.
    Returns:
        StudentService: An instance of the StudentService class.
    """
    return StudentService()
