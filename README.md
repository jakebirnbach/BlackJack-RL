# BlackJack-RL

A reinforcement learning project that implements blackjack from scratch and applies various RL techniques to train an agent that discovers the optimal playing strategy.

## Project Goals

- Implement a full blackjack game engine with standard casino rules
- Build an RL environment wrapper compatible with the Gymnasium observation space
- Implement and compare multiple RL algorithms (Monte Carlo, TD learning, Q-learning, etc.)
- Train agents that learn the optimal blackjack strategy through self-play

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Running

```bash
python -m src --sandbox
```

## Running Tests

```bash
python -m unittest discover -s tests -v
```

## Project Structure

```
src/
├── domain/                # Pure business objects — no external dependencies
│   ├── constants.py       # Suit, Rank, Action, Outcome enums
│   └── models.py          # Card, Hand, Deck, GameState
│
├── application/           # Use cases and orchestration — depends on domain only
│   ├── blackjack/
│   │   ├── game.py        # BlackjackGame — manages a single hand
│   │   └── game_orchestrator.py  # GameOrchestrator — manages shoes and sessions
│   ├── strategies/
│   │   ├── base_strategy.py      # BaseStrategy ABC
│   │   └── hit17_strategy.py     # Hit until 17 strategy
│   └── agents/
│       └── ...            # RL agent implementations (planned)
│
├── execution/             # Entry points for different run modes
│   └── execute_sandbox.py
│
└── infrastructure/        # External concerns (persistence, logging — future)
```

Follows **Clean Architecture** — dependencies point inward (infrastructure -> application -> domain).

## Game Rules (V1)

- Standard blackjack: player vs dealer
- Actions: hit, stand, or double down
- Dealer stands on soft 17 (configurable)
- Natural blackjack pays 3:2 or 6:5 (configurable)
- Shoe management with random cut card (60-80% penetration)
- No splitting or insurance (planned for future versions)