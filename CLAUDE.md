# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Peg solitaire game built with Python and Tkinter. Currently in early development — only the UI shell exists with no game logic implemented yet.

## Running the Application

```bash
python3 main.py
```

No external dependencies — uses only Python standard library (tkinter). Requires Python 3.12+. No tests, build steps, or linting configured.

## Architecture

The app uses a hierarchical Tkinter widget structure:

```
App (Tk root, 1280x720) → main_window (PanedWindow, 33/67 split)
  ├── menu_view (left pane) — stub, not yet implemented
  └── game_section (right pane)
      ├── counter_view — displays moves_made and pegs_remaining labels
      └── game_grid — 10x10 button grid (size passed from main.py)
```

- **main.py**: Entry point. Creates the App class (extends Tk) and instantiates main_window.
- **View/main_window.py**: Sets up a horizontal PanedWindow splitting menu and game areas. Also contains module-level test code that runs on import.
- **View/game_section.py**: Container composing counter_view and game_grid.
- **View/game_grid.py**: Generates an NxN grid of buttons. The `onclick` handler is currently undefined.
- **View/counter_view.py**: Two labels with hardcoded initial values (0 moves, 50 pegs). No update mechanism yet.
- **View/menu_view.py**: Minimal stub.

## Known Issues

- `game_grid.py` references an undefined `onclick` function in button commands
- `menu_view.py` has a bad import (`from tkinter import tkinter`)
- `main_window.py` has execution code at module level outside the class
- No game logic (move validation, win/loss detection) exists yet
- TODO: Clean up module-level test code in View files and switch to `from View import <Class>` imports once individual widget development is done

## Guidelines
- Project uses MVC pattern, separating logic and visuals
- Keep all written code to just snippets. Any tasks that require more than just a few lines should have the logic outlined instead
- When requested to "grade" or "check" a class/the project as a whole, refer to the Rubric section of `CLAUDE.md` to keep the project on track. Provide a percentage grade and what to do to improve.

## Rubric
- Project effectively uses Object-Oriented Programming
- Project is sufficiently modular
- Game logic and Visual logic are separate from each other
- Refer to any of the Known Issues in `CLAUDE.md` pertaining to the respective class(es) in question while grading
