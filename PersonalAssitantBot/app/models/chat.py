from pydantic import BaseModel

class Chat(BaseModel):
    thread_id : str | None = 'common'
    message : str

