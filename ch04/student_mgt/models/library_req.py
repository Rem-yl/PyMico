from datetime import datetime

from pydantic import BaseModel


class BookRequestReq(BaseModel):
    book_id: int
    request_date: datetime
    status: bool


class BookIssuanceReq(BaseModel):
    req_id: int
    approved_by: str
    approved_date: datetime


class BookReturnReq(BaseModel):
    issue_id: int
    returned_date: datetime
