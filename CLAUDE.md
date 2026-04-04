# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Blackjack reinforcement learning project: a from-scratch blackjack game engine that will serve as an RL environment for training agents to discover optimal play strategy. Currently in active development — the game engine is being built out, RL agents are not yet implemented.

## Development Setup

- Python 3.13, virtualenv at `.venv/`
- `pyproject.toml` manages package config — install with `pip install -e .`
- Activate: `source .venv/bin/activate`

## Running

```bash
python -m src --sandbox
```

## Running Tests

```bash
python -m unittest discover -s tests -v
```

Run a single test file:
```bash
python -m unittest tests.test_domain.test_models
```

Test directories are prefixed with `test_` (e.g., `tests/test_domain/`) to avoid shadowing source packages.

## Architecture

Clean Architecture with inward-pointing dependencies: `infrastructure → application → domain`.

**Domain layer** (`src/domain/`) — pure business objects, no external dependencies:
- `constants.py`: `Suit`, `Rank`, `Action`, `Outcome` enums. `Rank.points` property handles face card → 10 and ace → 11 mapping. `Outcome` values (1/-1/0) map directly to RL reward signals.
- `models.py`: `Card`, `Deck` (seeded RNG for reproducibility), `Hand` (auto-downgrades aces to avoid bust), `GameState` (frozen dataclass snapshot for agent decisions).
- `player.py`: `Player` (bankroll, betting, hand management). `Dealer` extends `Player` with `stand_on_17` flag.

**Application layer** (`src/application/`):
- `blackjack/game.py`: `BlackJackGame` — single hand lifecycle: betting → deal → player turn → dealer turn → payout. All game-deciding methods return `Outcome | None` (`None` = hand continues).
- `blackjack/game_orchestrator.py`: `GameOrchestrator` — manages shoe-level play with `play_hand` and `play_shoe`. Handles cut card (60-80% penetration) and reshuffling.
- `strategies/`: `BaseStrategy` ABC defines the `action(GameState) -> Action` interface. Concrete strategies (e.g., `Hit17Strategy`) inherit from it. This is the integration point for RL agents.

**Execution layer** (`src/execution/`): Entry points for different run modes. `--sandbox` flag runs smoke tests via `execute_sandbox.py`.
