# data_structs.py
import datetime
from dataclasses import dataclass, field
from typing import List


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

    def __str__(self):
        return (f'{self.name:30}\t{self.volume:>10,}\t(id={self.id})' + '\n' * (len(self.tweets) > 0) +
                '\n'.join(['\t\t* ' + tweet[:75].strip().replace("\n", " ") + '...' * (len(tweet) > 75) for tweet in
                           self.tweets]))


@dataclass
class DailyTopics:
    time: datetime
    topics: List[Topic]

    def __str__(self):
        return (f'{self.time}\t ({len(self.topics)} topics)'
                + '\n'
                + '\n'.join(['\t' + str(topic) for topic in self.topics])
                )


@dataclass
class DailyVolume:
    time: datetime
    volume: int


@dataclass
class TopicSummary:
    id: int
    name: str
    total_volume: int
    total_days: int
    first_date: datetime.date
    last_date: datetime.date

    def __str__(self):
        return f'{self.name[:15]}\t{self.total_volume:>10,} tweets\t{self.total_days:>3} days\t{self.first_date.strftime("%d/%m/%Y")}>{self.last_date.strftime("%d/%m/%Y")}'
