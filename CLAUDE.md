# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Blackjack reinforcement learning project: a from-scratch blackjack game engine that will serve as an RL environment for training agents to discover optimal play strategy. Currently in active development — the game engine is being built out, RL agents are not yet implemented.

## Development Setup

- Python 3.13, virtualenv at `.venv/`
- No package manager config (no pyproject.toml/requirements.txt yet) — stdlib only so far
- Activate: `source .venv/bin/activate`

## Running Tests

Tests use `unittest`. There is currently a **module import conflict**: source files use bare imports (`from domain.constants import ...`) while tests import via `src.` prefix (`from src.domain.models import ...`). Tests do not pass out of the box — this needs to be resolved.

```bash
# This is the intended command but currently fails due to import path mismatch:
python -m unittest discover -s tests -v
```

Run a single test file:
```bash
python -m unittest tests.domain.test_models
```

## Architecture

Clean Architecture with inward-pointing dependencies: `infrastructure → application → domain`.

**Domain layer** (`src/domain/`) — pure business objects, no external dependencies:
- `constants.py`: `Suit`, `Rank`, `Action` enums. `Rank.points` property handles face card → 10 and ace → 11 mapping.
- `models.py`: `Card`, `Deck` (seeded RNG for reproducibility), `Hand` (auto-downgrades aces to avoid bust), `GameState` (frozen dataclass snapshot for agent decisions).
- `player.py`: `Player` (bankroll, betting, hand management). `Dealer` extends `Player` with `stand_on_17` flag.

**Application layer** (`src/application/`):
- `blackjack/game.py`: `BlackJackGame` — full round lifecycle: betting → deal → player turn → dealer turn → payout. Player turn accepts a `Callable[[GameState], Action]` strategy function, which is the integration point for RL agents.
- `blackjack/game_orchestrator.py`: `GameOrchestrator` — wires a game with a strategy function (stub, in progress).
- `agents/`: Placeholder for RL agent implementations.

**Key design decision**: Agent strategies are injected as callables taking `GameState` and returning `Action`. This decouples the game engine from any specific RL framework.
