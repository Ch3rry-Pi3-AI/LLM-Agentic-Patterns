"""
prompts.py
----------
System prompts and small helpers for the Reflection pattern.

This module centralises the default system prompts used by the ReflectionAgent.
Keeping them here makes it easy to reuse/extend or swap them in tests.
"""

# -------------------------------------------------------------------
# Base System Prompts
# -------------------------------------------------------------------

BASE_GENERATION_SYSTEM_PROMPT: str = """
Your task is to Generate the best content possible for the user's request.
If the user provides critique, respond with a revised version of your previous attempt.
You must always output the revised content.
"""

BASE_REFLECTION_SYSTEM_PROMPT: str = """
You are tasked with generating critique and recommendations to the user's generated content.
If the user content has something wrong or something to be improved, output a list of recommendations
and critiques. If the user content is ok and there's nothing to change, output this: <OK>
"""


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def compose_prompt(custom: str | None, base: str) -> str:
    """
    Compose a custom system prompt with the base system prompt.

    Parameters
    ----------
    custom : str | None
        Optional custom system prompt to prepend.
    base : str
        The base system prompt to append.

    Returns
    -------
    str
        The combined system prompt.
    """
    return (custom or "") + base