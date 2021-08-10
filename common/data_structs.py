# data_structs.py
import datetime
from dataclasses import dataclass, field
from typing import List

from collections import namedtuple

@dataclass
class UniqueTopic:
    id: int
    base_name: str
    display_name: str
    dirty: bool = False


@dataclass
class Topic:
    id: int
    name: str
    volume: int
    tweets: List[str] = field(default=lambda: [])


@dataclass
class DailyTopics:
    time: datetime
    topics: List[Topic]


@dataclass
class TopicSummary:
    id: int
    name: str
    total_volume: int
    total_days: int
    first_date: datetime.date
    last_date: datetime.date
