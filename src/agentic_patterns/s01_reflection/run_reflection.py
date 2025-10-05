"""
run_reflection.py
-----------------
Convenience entry-point to exercise the ReflectionAgent from code or CLI.

Usage
-----
Python API (from inside the same package):
    # If you are calling this from another module inside the
    # 'agentic_patterns/s01_reflection' package, use relative imports:
    from .agent import ReflectionAgent
    from .settings import ModelConfig

    agent = ReflectionAgent(ModelConfig(model="llama-3.3-70b-versatile"))
    result = agent.run("Write a short poem about modular code.", n_steps=5, verbose=1)
    print(result)

CLI (file-path invocation works even without package context):
    python src/agentic_patterns/s01_reflection/run_reflection.py \
        --message "Write a short poem about modular code." \
        --steps 5 --verbose 1 --model llama-3.3-70b-versatile

Note
----
If you prefer module execution:
    python -m agentic_patterns.s01_reflection.run_reflection --message "..." --steps 5
"""

from __future__ import annotations

# -------------------------------------------------------------------
# Standard Library
# -------------------------------------------------------------------
import argparse

# -------------------------------------------------------------------
# Internal Imports (support both module and script execution)
# -------------------------------------------------------------------
try:
    # Works when executed as a module: `python -m agentic_patterns.s01_reflection.run_reflection`
    from .agent import ReflectionAgent
    from .settings import ModelConfig
except ImportError:
    # Fallback for direct file execution:
    # `python src/agentic_patterns/s01_reflection/run_reflection.py`
    import sys
    from pathlib import Path

    # Path layout: .../src/agentic_patterns/s01_reflection/run_reflection.py
    # parents[2] -> .../src
    src_dir = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(src_dir))

    from agentic_patterns.s01_reflection.agent import ReflectionAgent  # type: ignore
    from agentic_patterns.s01_reflection.settings import ModelConfig  # type: ignore


# -------------------------------------------------------------------
# CLI Entrypoint
# -------------------------------------------------------------------

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

    # Construct and execute the agent.
    agent = ReflectionAgent(model_cfg=ModelConfig(model=args.model))
    final = agent.run(args.message, n_steps=args.steps, verbose=args.verbose)

    # Pretty-print the final output.
    print("\n" + "=" * 80 + "\nFINAL OUTPUT\n" + "=" * 80 + f"\n{final}\n")


if __name__ == "__main__":
    main()