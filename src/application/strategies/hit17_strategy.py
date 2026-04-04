from application.strategies.base_strategy import BaseStrategy
from domain.constants import Action
from domain.models import GameState

class Hit17Strategy(BaseStrategy):
    def action(self, curr_state: GameState) -> Action:
        return Action.HIT if curr_state.player_value < 17 else Action.STAND