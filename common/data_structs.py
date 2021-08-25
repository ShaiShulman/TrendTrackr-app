# data_structs.py
""" Data structures used in the model"""
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
    tweets: List[str]  # = field(default=lambda: [])

    def __str__(self):
        return (f'{self.name:30}\t{self.volume:>10,}\t(id={self.id})' + '\n' * (len(self.tweets) > 0) +
                '\n'.join(['\t\t* ' + tweet[:75].strip().replace("\n", " ") + '...' * (len(tweet) > 75) for tweet in
                           self.tweets]))


@dataclass
class TopicStat(Topic):
    """
    Topic for a specific date with statistical analysis
    """
    rank: int
    pct_volume: float

    def __str__(self):
        return (
                    f'{self.name:30}\t{self.volume:>10,}\t{self.rank:>4} rank\t({self.pct_volume:.2%})\t(id={self.id})' + '\n' * (
                        len(self.tweets) > 0) +
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
        return f'{self.time}\t{self.volume:>10,} tweets ({self.pct_volume:.2%})\t{self.rank:>2} rank\t'


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
        return f'{self.name:<25}\t{self.total_volume:>10,} tweets\t{self.total_days:>3} days\t{self.first_date.strftime("%d/%m/%Y")}>{self.last_date.strftime("%d/%m/%Y")} '

    # comparer used for sorting in a list of topics
    def __lt__(self, other):
        return (self.name[:1].replace('#', '') + self.name[1:]).lower() < (other.name[:1].replace('#', '') + other.name[1:]).lower()
