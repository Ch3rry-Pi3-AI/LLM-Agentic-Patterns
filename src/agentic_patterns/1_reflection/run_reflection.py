"""
run_reflection.py
-----------------
Convenience entry-point to exercise the ReflectionAgent from code or CLI.

Usage
-----
Python API:
    from src.1_reflection.agent import ReflectionAgent
    from src.1_reflection.settings import ModelConfig

    agent = ReflectionAgent(ModelConfig(model="llama-3.3-70b-versatile"))
    result = agent.run("Write a short poem about modular code.", n_steps=5, verbose=1)
    print(result)

CLI:
    python -m src.1_reflection.run_reflection \
        --message "Write a short poem about modular code." \
        --steps 5 --verbose 1 --model llama-3.3-70b-versatile
"""

from __future__ import annotations

# -------------------------------------------------------------------
# Standard Library
# -------------------------------------------------------------------
import argparse

# -------------------------------------------------------------------
# Internal Imports
# -------------------------------------------------------------------
from .agent import ReflectionAgent
from .settings import ModelConfig


def main() -> None:
    """
    Parse CLI arguments and run the ReflectionAgent.
    """
    parser = argparse.ArgumentParser(description="Run the Reflection pattern loop.")
    parser.add_argument(
        "--message",
        required=True,
        help="User message to seed the generation loop.",
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=10,
        help="Maximum number of generate–reflect cycles (default: 10).",
    )
    parser.add_argument(
        "--verbose",
        type=int,
        default=0,
        help="Verbosity level (0 = quiet).",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="llama-3.3-70b-versatile",
        help="Model name to use.",
    )
    args = parser.parse_args()

    agent = ReflectionAgent(model_cfg=ModelConfig(model=args.model))
    final = agent.run(args.message, n_steps=args.steps, verbose=args.verbose)
    print("\n" + "=" * 80 + "\nFINAL OUTPUT\n" + "=" * 80 + f"\n{final}\n")


if __name__ == "__main__":
    main()