"""
completions.py
--------------
Utility functions and helper classes for interacting with Groq language models
and maintaining conversation histories.

This module abstracts the low-level interaction with the model client, as well as
the management of chat message queues used throughout the agentic framework.

British English spelling is used for documentation and comments.
"""

from __future__ import annotations

# -------------------------------------------------------------------
# Third-Party Imports
# -------------------------------------------------------------------
from groq import Groq


# -------------------------------------------------------------------
# Model Interaction Utilities
# -------------------------------------------------------------------

def completions_create(client: Groq, messages: list[dict], model: str) -> str:
    """
    Send a request to the Groq client's `chat.completions.create` endpoint.

    Parameters
    ----------
    client : Groq
        The Groq client object used to make the request.
    messages : list of dict
        List of message objects forming the conversation history for the model.
        Each message should include 'role' and 'content' keys.
    model : str
        The name of the model to use for generating completions.

    Returns
    -------
    str
        The textual content returned by the model.
    """
    response = client.chat.completions.create(messages=messages, model=model)
    return str(response.choices[0].message.content)


# -------------------------------------------------------------------
# Prompt & Message Structuring
# -------------------------------------------------------------------

def build_prompt_structure(prompt: str, role: str, tag: str = "") -> dict:
    """
    Build a structured prompt entry including the role and content.

    Parameters
    ----------
    prompt : str
        The text content of the prompt.
    role : str
        The role of the speaker (e.g., 'user', 'assistant', 'system').
    tag : str, optional
        Optional XML-style tag to wrap around the prompt content.

    Returns
    -------
    dict
        A dictionary representing the structured prompt message.
    """
    if tag:
        prompt = f"<{tag}>{prompt}</{tag}>"
    return {"role": role, "content": prompt}


def update_chat_history(history: list, msg: str, role: str) -> None:
    """
    Append a new message to the chat history.

    Parameters
    ----------
    history : list
        The list representing the current chat history.
    msg : str
        The message to append.
    role : str
        The message role ('user', 'assistant', or 'system').
    """
    history.append(build_prompt_structure(prompt=msg, role=role))


# -------------------------------------------------------------------
# Chat History Containers
# -------------------------------------------------------------------

class ChatHistory(list):
    """
    A simple bounded list for storing message history.

    This class behaves like a queue, automatically discarding the oldest
    message when the total length limit is reached.

    Attributes
    ----------
    total_length : int
        The maximum number of messages the chat history can hold.
    """

    def __init__(self, messages: list | None = None, total_length: int = -1) -> None:
        """Initialise the queue with an optional total length."""
        if messages is None:
            messages = []
        super().__init__(messages)
        self.total_length = total_length

    def append(self, msg: str) -> None:
        """
        Add a message to the queue, discarding the oldest if full.

        Parameters
        ----------
        msg : str
            The message to add to the queue.
        """
        if len(self) == self.total_length:
            self.pop(0)
        super().append(msg)


class FixedFirstChatHistory(ChatHistory):
    """
    Chat history variant that keeps the first message fixed.

    Useful for maintaining the system prompt while limiting context growth.

    Attributes
    ----------
    total_length : int
        The maximum number of messages (including the fixed one).
    """

    def append(self, msg: str) -> None:
        """
        Add a message to the queue, always preserving the first message.

        Parameters
        ----------
        msg : str
            The message to add to the queue.
        """
        if len(self) == self.total_length:
            # Pop the second message instead of the first, keeping the system prompt fixed.
            self.pop(1)
        super().append(msg)