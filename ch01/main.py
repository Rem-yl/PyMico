from typing import Dict, Union
from uuid import UUID

from bcrypt import checkpw
from fastapi import FastAPI
from model import ForumDiscussion, User, UserProfile, ValidUser

app = FastAPI()

valid_users: Dict[str, ValidUser] = {}
pending_users: Dict[str, User] = {}
valid_profile: Dict[str, UserProfile] = {}
disscussion_posts: Dict[UUID, ForumDiscussion] = {}


@app.get("/ch01/index")
def index() -> Dict[str, str]:
    return {"message": "Welcome to FastAPI demo"}


@app.get("/ch01/login/")
def login(username: str, password: str) -> Union[Dict[str, str], ValidUser]:
    user = valid_users.get(username)
    if user is None:
        return {"message": f"user: {username} does not exist"}

    if checkpw(password.encode(), user.passphrase.encode()):
        return user

    return {"message": f"invalid user: {username}"}


@app.post("/ch01/login/signup")
def signup(username: str, password: str) -> Union[Dict[str, str], User]:
    if username is None and password is None:
        return {"message": f"invalid user: {username}"}

    if valid_users.get(username) is not None:
        return {"message": f"user: {username} exists"}

    user = User(username=username, password=password)
    pending_users[username] = user
    return user


@app.put("/ch01/account/profile/update/{username}")
def update_profile(
    username: str, user_id: UUID, profile: UserProfile
) -> Dict[str, str]:
    user = valid_users.get(username)
    if user is None:
        return {"message": f"user: {username} exists"}

    if user.id == user_id:
        valid_profile[username] = profile
        return {"message": f"user: {username} profile update success"}

    return {"message": f"user: {username} does not exist"}


@app.put("/ch01/account/profile/update/{username}")
def update_profile_name(
    username: str, user_id: UUID, name: Dict[str, str]
) -> Dict[str, str]:
    user = valid_users.get(username)

    if user is None:
        return {"message": f"user: {username} does not exist"}

    if name is None:
        return {"message": "new name need required"}

    if user.id == user_id:
        profile = valid_profile[username]
        profile.firstname = name["fname"]
        profile.lastname = name["lname"]
        profile.middle_initial = name["mi"]
        valid_profile[username] = profile

        return {"message": "profile update success"}

    return {"message": f"user: {username} does not exist"}


@app.delete("/ch01/remove/{username}")
def delete_discussion(username: str, uuid: UUID) -> Dict[str, str]:
    if valid_users.get(username) is None:
        return {"message": f"user: {username} does not exist"}

    if disscussion_posts.get(uuid) is None:
        return {"message": "post does not exist"}

    del disscussion_posts[uuid]
    return {"message": "main post deleted"}
