from pydantic import BaseModel


class Data(BaseModel):
    input_data: str
