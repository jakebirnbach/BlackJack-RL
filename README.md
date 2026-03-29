# BlackJack-RL

A reinforcement learning project that implements blackjack from scratch and applies various RL techniques to train an agent that discovers the optimal playing strategy.

## Project Goals

- Implement a full blackjack game engine with standard casino rules
- Build an RL environment wrapper compatible with the Gymnasium observation space
- Implement and compare multiple RL algorithms (Monte Carlo, TD learning, Q-learning, etc.)
- Train agents that learn the optimal blackjack strategy through self-play

## Project Structure

```
src/
├── domain/                # Pure business objects — no external dependencies
│   ├── constants.py       # Suits, ranks, card values
│   ├── enums.py           # GameResult and other enumerations
│   └── models.py          # Card, Hand, Deck
│
├── application/           # Use cases and orchestration — depends on domain only
│   ├── blackjack/
│   │   └── game.py        # BlackjackGame — manages a round of play
│   └── agents/
│       └── ...            # RL agent implementations
│
└── infrastructure/        # External concerns (persistence, logging — future)

notebooks/                 # Experimentation, visualization, learning curves
```

Follows **Clean Architecture** — dependencies point inward (infrastructure -> application -> domain).

## Game Rules (V1)

- Standard blackjack: player vs dealer
- Actions: hit or stand
- Dealer stands on soft 17
- Natural blackjack pays 1.5x
- No splitting, doubling, or insurance (planned for future versions)