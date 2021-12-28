from dataclasses import dataclass


def get_feed_per_day(staked_egg: float) -> float:
    """get the number of feed per day based on the staked $egg"""
    return 3 * staked_egg


@dataclass
class EggStake:
    staked_eggs: float

    @property
    def feeds_per_day(self):
        return get_feed_per_day(self.staked_eggs)

    def add_eggs(self, eggs: float):
        self.staked_eggs += eggs
