from typing import Any, Dict, List, Optional, Union
from uuid import UUID, uuid1

from bcrypt import checkpw, gensalt, hashpw
from fastapi import FastAPI, Header
from model import (
    ForumDiscussion,
    ForumPost,
    Post,
    PostType,
    User,
    UserProfile,
    ValidUser,
)

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


@app.get("/ch01/login/details/info")
def login_info() -> Dict[str, str]:
    return {"message": "username and password are needed"}


@app.delete("/ch01/login/remove/{username}")
def delete_user(username: str) -> Dict[str, str]:
    if username is None:
        return {"message": "invalid user"}

    if valid_users.get(username) is None:
        return {"message": f"user: {username} does not exist"}

    del valid_users[username]
    return {"message": f"user: {username} deleted"}


@app.delete("/ch01/login/remove/all")
def delete_users(username: List[str]) -> Dict[str, str]:
    for user in username:
        del valid_users[user]

    return {"message": "deleted users"}


@app.delete("/ch01/delete/users/pending")
def delete_pending_users(accounts: Optional[List[str]] = None) -> Dict[str, str]:
    if accounts is None:
        accounts = []

    for user in accounts:
        del pending_users[user]

    return {"message": "deleted pending users"}


@app.post("/ch01/login/username/unlock")
def unlock_username(user_id: Optional[UUID] = None) -> Dict[str, Optional[str]]:
    if id is None:
        return {"message": "token needed"}

    for _, val in valid_users.items():
        if val.id == user_id:
            return {"username": val.username}

    return {"message": "user does not exist"}


@app.post("/ch01/login/validate", response_model=ValidUser)
def approve_user(user: User) -> ValidUser:
    if valid_users.get(user.username) is not None:
        return ValidUser(id=None, username=None, password=None, passphrase=None)

    valid_user = ValidUser(
        id=uuid1(),
        username=user.username,
        password=user.password,
        passphrase=hashpw(user.password.encode(), gensalt()).decode("utf-8"),
    )

    valid_users[user.username] = valid_user
    del pending_users[user.username]

    return valid_user


@app.get("/ch01/header/verify")
def verify_headers(
    host: Optional[str] = Header(None),
    accept: Optional[str] = Header(None),
    accept_language: Optional[str] = Header(None),
    accept_encoding: Optional[str] = Header(None),
    user_agent: Optional[str] = Header(None),
) -> Dict[str, Any]:
    request_headers = {}
    request_headers["Host"] = host
    request_headers["Accept"] = accept
    request_headers["Accept-Language"] = accept_language
    request_headers["Accept-Encoding"] = accept_encoding
    request_headers["User-Agent"] = user_agent

    return request_headers


@app.post("/ch01/discussion/posts/add/{username}")
def post_discussion(
    username: str, user_id: UUID, post: Post, post_type: PostType
) -> Union[Dict[str, str], ForumDiscussion]:
    if valid_users.get(username) is None:
        return {"message": "user does not exist"}

    if disscussion_posts.get(user_id) is not None:
        return {"message": "post already exists"}

    forum_post = ForumPost(
        id=uuid1(),
        topic=post.topic,
        message=post.message,
        post_type=post_type,
        date_posted=post.date_posted,
        username=username,
    )
    user = valid_profile[username]
    forum = ForumDiscussion(id=uuid1(), main_post=forum_post, author=user, replies=[])
    disscussion_posts[forum.id] = forum

    return forum
