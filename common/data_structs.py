# data_structs.py
""" Data structures used in the app"""
import datetime
from dataclasses import dataclass, field
from typing import List


@dataclass
class UniqueTopic:
    """
    Topic in the topics master list
    """
    id: int
    base_name: str
    display_name: str
    dirty: bool = False


@dataclass
class Topic:
    """
    Trending topic intercepted on a specific date
    """
    id: int
    name: str
    volume: int
    rank: int
    pct_volume: float
    tweets: List[str] = field(default=lambda: [])

    def __str__(self):
        return (f'{self.name:30}\t{self.volume:>10,}\t{self.rank:<2} rank\t({self.pct_volume:.2%})\t(id={self.id})' + '\n' * (len(self.tweets) > 0) +
                '\n'.join(['\t\t* ' + tweet[:75].strip().replace("\n", " ") + '...' * (len(tweet) > 75) for tweet in
                           self.tweets]))


@dataclass
class DailyTopics:
    """
    Container class for topics intercepted on specific date
    """
    time: datetime
    topics: List[Topic]

    def __str__(self):
        return (f'{self.time}\t ({len(self.topics)} topics)'
                + '\n'
                + '\n'.join(['\t' + str(topic) for topic in self.topics])
                )


@dataclass
class DailyVolume:
    """
    Volume for a topic as intercepted on a specific date
    """
    time: datetime
    volume: int
    rank: int
    pct_volume: float

    def __str__(self):
        return f'{self.time}\t{self.volume:>10,} tweets ({self.pct_volume:.2f%})\t{self.rank:>2} rank\t'


@dataclass
class TopicSummary:
    """
    Summary stats for a topic
    """
    id: int
    name: str
    total_volume: int
    total_days: int
    first_date: datetime.date
    last_date: datetime.date

    def __str__(self):
        return f'{self.name[:15]}\t{self.total_volume:>10,} tweets\t{self.total_days:>3} days\t{self.first_date.strftime("%d/%m/%Y")}>{self.last_date.strftime("%d/%m/%Y")}'
