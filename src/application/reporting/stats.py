from domain.models import OutcomeOutput, OutputStats, GameState
from domain.constants import Outcome


class StatCalculator:
   @staticmethod
   def calculate_stats(outcomes: list[OutcomeOutput], starting_bankroll: float, ending_bankroll: float) -> OutputStats:
       if starting_bankroll < 0 or ending_bankroll < 0:
           raise ValueError("Starting and ending bankroll must be non-negative")
       if len(outcomes) < 1:
           raise ValueError("Number of outcomes must be greater than 0")

       hands_played: int = len(outcomes)
       wins: int = sum(1 for o in outcomes if o.outcome == Outcome.PLAYER_WIN)
       losses: int = sum(1 for o in outcomes if o.outcome == Outcome.DEALER_WIN)
       pushes: int = sum(1 for o in outcomes if o.outcome == Outcome.PUSH)
       total_wagered: float = sum(o.bet_amount for o in outcomes)
       total_payout: float = sum(o.payout for o in outcomes)
       profit: float = total_payout - total_wagered
       roi: float = profit / total_wagered if total_wagered > 0 else 0
       win_rate: float = wins / hands_played
       average_bet_amount: float = sum(o.bet_amount for o in outcomes) / hands_played

       return OutputStats(
           starting_bankroll = starting_bankroll,
           ending_bankroll = ending_bankroll,
           hands_played = hands_played,
           wins = wins,
           losses = losses,
           pushes = pushes,
           total_wagered = total_wagered,
           total_payout = total_payout,
           profit = profit,
           roi = roi,
           win_rate = win_rate,
           average_bet_amt=average_bet_amount
       )


