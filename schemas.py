from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Settings(BaseModel):
    # Remove spaces at the start/end of text before checking length.
    model_config = ConfigDict(str_strip_whitespace=True)

    nickname: str = Field(min_length=1, max_length=30)
    daily_goal_breaks: int = Field(ge=1, le=20)
    coaching_mode: Literal["focus", "coach"]
    sitting_interval_minutes: int = Field(ge=1, le=120)