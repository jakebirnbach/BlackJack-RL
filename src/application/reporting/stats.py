from domain.models import OutcomeOutput, OutputStats, GameState, AggregateStats
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

   @staticmethod
   def calculate_aggregate_stats(output_stats: list[OutputStats]) -> AggregateStats:
       total_shoes: int = len(output_stats)
       total_hands_played: int = sum(o.hands_played for o in output_stats)
       total_wins: int = sum(o.wins for o in output_stats)
       total_losses: int = sum(o.losses for o in output_stats)
       total_pushes: int = sum(o.pushes for o in output_stats)
       total_wagered: float = sum(o.total_wagered for o in output_stats)
       total_profit: float = sum(o.profit for o in output_stats)
       overall_roi: float = total_profit / total_wagered if total_wagered > 0 else 0
       overall_win_rate: float = total_wins / total_hands_played if total_hands_played > 0 else 0
       avg_profit_per_shoe: float = total_profit / total_shoes if total_shoes > 0 else 0
       std_dev_profit_per_shoe: float = (sum((o.profit - avg_profit_per_shoe)**2 for o in output_stats) / total_shoes) ** 0.5 if total_shoes > 0 else 0
       min_profit: float = min(o.profit for o in output_stats)
       max_profit: float = max(o.profit for o in output_stats)
       avg_hands_per_shoe: float = total_hands_played / total_shoes if total_shoes > 0 else 0
       min_ending_bankroll: float = min(o.ending_bankroll for o in output_stats)
       max_ending_bankroll: float = max(o.ending_bankroll for o in output_stats)

       return AggregateStats(
           total_shoes = total_shoes,
           total_hands_played = total_hands_played,
           total_wins = total_wins,
           total_losses = total_losses,
           total_pushes = total_pushes,
           total_wagered = total_wagered,
           total_profit = total_profit,
           overall_roi = overall_roi,
           overall_win_rate = overall_win_rate,
           avg_profit_per_shoe = avg_profit_per_shoe,
           std_dev_profit_per_shoe = std_dev_profit_per_shoe,
           min_profit = min_profit,
           max_profit = max_profit,
           avg_hands_per_shoe = avg_hands_per_shoe,
           min_ending_bankroll = min_ending_bankroll,
           max_ending_bankroll = max_ending_bankroll
       )

