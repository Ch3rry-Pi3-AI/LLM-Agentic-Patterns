"""
logging.py
----------
Utility functions for colourful console logging and progress visualisation.

These helpers provide lightweight, visually distinctive print outputs for use in
agent execution loops (e.g., the generation–reflection process).
"""

from __future__ import annotations

# -------------------------------------------------------------------
# Standard Library & Third-Party Imports
# -------------------------------------------------------------------
import time

from colorama import Fore, Style


# -------------------------------------------------------------------
# Fancy Printing Utilities
# -------------------------------------------------------------------

def fancy_print(message: str) -> None:
    """
    Display a stylised, colourised message to the console.

    Parameters
    ----------
    message : str
        The message text to display.
    """
    print(Style.BRIGHT + Fore.CYAN + f"\n{'=' * 50}")
    print(Fore.MAGENTA + f"{message}")
    print(Style.BRIGHT + Fore.CYAN + f"{'=' * 50}\n")
    time.sleep(0.5)


# -------------------------------------------------------------------
# Progress Tracking
# -------------------------------------------------------------------

def fancy_step_tracker(step: int, total_steps: int) -> None:
    """
    Display a formatted step tracker for iterative processes.

    Parameters
    ----------
    step : int
        The current step index (zero-based).
    total_steps : int
        The total number of steps in the loop.
    """
    fancy_print(f"STEP {step + 1}/{total_steps}")