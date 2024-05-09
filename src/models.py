from pydantic import BaseModel


class FooData(BaseModel):
    test: str


class BarData(BaseModel):
    something: int
