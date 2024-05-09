from enum import StrEnum
from types import NoneType
from typing import Annotated, Any, Literal, Union, get_args

from pydantic import BaseModel, Field

from src.models import BarData, FooData


class RedisChannelEnum(StrEnum):
    """Channels for Redis Pub/Sub"""

    BAR = "bar"
    FOO = "foo"


class BaseChannelMessage(BaseModel):
    type: Literal["message"] = "message"
    channel: RedisChannelEnum
    data: BaseModel

    @classmethod
    def _get_annotation(cls, lookup: Literal["channel", "data"]) -> Any:
        annotation = cls.model_fields[lookup].annotation
        if annotation == NoneType:  # none is annotated as NoneType
            return None
        return annotation

    @classmethod
    def get_channel(cls) -> RedisChannelEnum:
        topic = cls._get_annotation("channel")
        return get_args(topic)[0]


class FooChannel(BaseChannelMessage):
    """Foo Channel"""

    channel: Literal[RedisChannelEnum.FOO] = RedisChannelEnum.FOO
    data: FooData


class BarChannel(BaseChannelMessage):
    """Bar Channel"""

    channel: Literal[RedisChannelEnum.BAR] = RedisChannelEnum.BAR
    data: BarData


RedisChannels = Annotated[Union[FooChannel, BarChannel], Field(discriminator="channel")]
