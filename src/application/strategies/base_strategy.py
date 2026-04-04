from abc import ABC, abstractmethod
from domain.constants import Action
from domain.models import GameState

class BaseStrategy(ABC):
    @abstractmethod
    def action(self, curr_state: GameState) -> Action:
        pass
