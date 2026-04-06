from enum import Enum, IntEnum

# Suit Enums
class Suit(Enum):
    SPADE = 'Spade'
    CLUB = 'Club'
    DIAMOND = 'Diamond'
    HEART = 'Heart'

# Rank Enum
class Rank(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    @property
    def points(self) -> int:
        if self in (Rank.JACK, Rank.QUEEN, Rank.KING):
            return 10
        if self == Rank.ACE:
            return 11
        return self.value


class Action(Enum):
    HIT = "Hit"
    STAND = "Stand"
    DOUBLE_DOWN = "Double Down"


class Outcome(Enum):
    PLAYER_WIN = 1
    DEALER_WIN = -1
    PUSH = 0