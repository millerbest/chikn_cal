from dataclasses import dataclass, field


def get_egg_per_day(level: int) -> float:
    """get the number of $egg per day based on the level (weight) of the chicken"""
    return 1 + 0.25 * (level - 1)


def get_feed_for_upgrade(current_level: int):
    """get the need feed for a chicken to upgrade to the next level"""
    return 25 * current_level ** 2


@dataclass
class Chicken:
    base_price: float  # the price for the chicken in USDT
    level: int  # the weight of the chicken
    feeding_progress: int = 0  # how much the chicken has been feeded

    @property
    def egg_per_day(self) -> float:
        return get_egg_per_day(self.level)

    @property
    def max_feed(self) -> int:
        return get_feed_for_upgrade(self.level)

    def feed(self, amount: float) -> None:
        self.feeding_progress += amount
        while self.feeding_progress >= self.max_feed:
            self.feeding_progress -= self.max_feed
            self.level += 1
        return


if __name__ == "__main__":
    chicken = Chicken(base_price=100, level=1)
