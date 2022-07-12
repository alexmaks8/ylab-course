from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Generator, List, Tuple


@dataclass
class Movie:
    title: str
    dates: List[Tuple[datetime, datetime]]

    def schedule(self) -> Generator[datetime, None, None]:
        days = []
        for n in range(len(self.dates)):
            for day in range((self.dates[n][1] - self.dates[n][0]).days + 1):
                date = self.dates[n][0]
                date += timedelta(days=day)
                days.append(date)

        return days


if __name__ == '__main__':
    m = Movie('sw', [
    (datetime(2020, 1, 1), datetime(2020, 1, 7)),
    (datetime(2020, 1, 15), datetime(2020, 2, 7))
    ])

    for d in m.schedule():
        print(d)
