from dataclasses import dataclass


@dataclass
class Feeds:
    amount: float = 0

    def add_feeds(self, num_feeds: float) -> None:
        self.amount += num_feeds

    def use_feeds(self, num_feeds: float) -> None:
        if self.amount - num_feeds < 0:
            raise ValueError("not enough feeds to consume")
        else:
            self.amount -= num_feeds
