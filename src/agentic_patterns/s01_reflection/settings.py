"""
settings.py
-----------
Client and model setup for the Reflection pattern.

This module isolates environment loading and client construction so that:
- the agent stays focused on orchestration, and
- tests can inject a mock client easily.
"""

from __future__ import annotations

# -------------------------------------------------------------------
# Standard Library & Third-Party Imports
# -------------------------------------------------------------------
from dataclasses import dataclass

from dotenv import load_dotenv
from groq import Groq


# -------------------------------------------------------------------
# Environment / Defaults
# -------------------------------------------------------------------

# Load .env once on import so downstream modules do not need to.
load_dotenv()


@dataclass(frozen=True)
class ModelConfig:
    """
    Lightweight configuration container for model/runtime parameters.

    Attributes
    ----------
    model : str
        Model name to use for both generation and reflection.
    """
    model: str = "llama-3.3-70b-versatile"


def get_groq_client() -> Groq:
    """
    Construct a Groq client instance.

    Returns
    -------
    Groq
        A ready-to-use Groq client.
    """
    # If you ever need to parameterise (timeouts, api_base, etc.),
    # do it here to keep the agent code clean.
    return Groq()