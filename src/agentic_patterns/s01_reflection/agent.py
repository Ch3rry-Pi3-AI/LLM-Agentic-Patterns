"""
agent.py
--------
ReflectionAgent: generate -> reflect -> (optionally) iterate.

This is a modularised version of the original script, with the logic preserved
and dependencies injected where sensible.

Notes
-----
- Uses existing utilities:
    agentic_patterns.utils.completions.{build_prompt_structure, completions_create,
                                        FixedFirstChatHistory, update_chat_history}
    agentic_patterns.utils.logging.fancy_step_tracker
- System prompts are imported from `prompts.py`.
- Client/model setup is isolated in `settings.py`.

British English spelling is used for docs/comments where applicable.
"""

from __future__ import annotations

# -------------------------------------------------------------------
# Standard Library & Third-Party Imports
# -------------------------------------------------------------------
from typing import List

from colorama import Fore

# -------------------------------------------------------------------
# Internal Imports
# -------------------------------------------------------------------
from agentic_patterns.utils.completions import (
    build_prompt_structure,
    completions_create,
    FixedFirstChatHistory,
    update_chat_history,
)
from agentic_patterns.utils.logging import fancy_step_tracker

from .prompts import (
    BASE_GENERATION_SYSTEM_PROMPT,
    BASE_REFLECTION_SYSTEM_PROMPT,
    compose_prompt,
)
from .settings import get_groq_client, ModelConfig


# -------------------------------------------------------------------
# ReflectionAgent
# -------------------------------------------------------------------

class ReflectionAgent:
    """
    Orchestrates an iterative loop of:
        1) Generation (assistant role),
        2) Reflection/critique (assistant role),
        3) Optional early stop if critique returns the sentinel "<OK>".

    Parameters
    ----------
    model_cfg : ModelConfig, optional
        Model configuration holding the model name to use.
    client : Any, optional
        A Groq-compatible client providing a `chat.completions.create` API.
        By default, a Groq client is constructed via `get_groq_client()`.

    Attributes
    ----------
    model : str
        The model name to use.
    client : Any
        The LLM client used to create completions.
    """

    def __init__(self, model_cfg: ModelConfig | None = None, client=None) -> None:
        # Keep the model name configurable but default to ModelConfig.
        self.model = (model_cfg or ModelConfig()).model
        # Allow DI of the client for testing; default to a real Groq client.
        self.client = client or get_groq_client()

    # -------------------------------------------------------------------
    # Private Helpers
    # -------------------------------------------------------------------
    def _request_completion(
        self,
        history: List[dict],
        *,
        verbose: int = 0,
        log_title: str = "COMPLETION",
        log_color: str = "",
    ) -> str:
        """
        Request a completion from the LLM.

        Parameters
        ----------
        history : list of dict
            The (role, content) message history to send.
        verbose : int, default=0
            If > 0, pretty-prints the model output.
        log_title : str, default="COMPLETION"
            Title used in verbose logs.
        log_color : str, default=""
            ANSI colour from `colorama.Fore` for the verbose title.

        Returns
        -------
        str
            The model-generated content.
        """
        # Delegate actual inference to the shared utility.
        output = completions_create(self.client, history, self.model)
        if verbose > 0:
            print(log_color, f"\n\n{log_title}\n\n", output)
        return output

    # -------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------
    def generate(self, generation_history: List[dict], *, verbose: int = 0) -> str:
        """
        Generate a response for the current user intent.

        Parameters
        ----------
        generation_history : list of dict
            Message history for generation (system + user + prior assistant).
        verbose : int, default=0
            Verbosity level.

        Returns
        -------
        str
            The generated content.
        """
        return self._request_completion(
            generation_history, verbose=verbose, log_title="GENERATION", log_color=Fore.BLUE
        )

    def reflect(self, reflection_history: List[dict], *, verbose: int = 0) -> str:
        """
        Produce a critique/recommendations for the latest generation.

        Parameters
        ----------
        reflection_history : list of dict
            Message history for reflection (system + alternating user/assistant).
        verbose : int, default=0
            Verbosity level.

        Returns
        -------
        str
            The reflection/critique content.
        """
        return self._request_completion(
            reflection_history, verbose=verbose, log_title="REFLECTION", log_color=Fore.GREEN
        )

    def run(
        self,
        user_msg: str,
        *,
        generation_system_prompt: str | None = None,
        reflection_system_prompt: str | None = None,
        n_steps: int = 10,
        verbose: int = 0,
    ) -> str:
        """
        Execute the reflection loop for up to `n_steps` iterations.

        Parameters
        ----------
        user_msg : str
            The user's initial request.
        generation_system_prompt : str | None, optional
            Optional custom system prompt for generation. The base prompt is
            always appended.
        reflection_system_prompt : str | None, optional
            Optional custom system prompt for reflection. The base prompt is
            always appended.
        n_steps : int, default=10
            Maximum number of generate–reflect cycles to attempt.
        verbose : int, default=0
            Verbosity level; if > 0, prints coloured stage banners.

        Returns
        -------
        str
            The final generated content (last "assistant" output from generation).
        """
        # Combine any caller-supplied prompts with the defaults.
        gen_sys_prompt = compose_prompt(generation_system_prompt, BASE_GENERATION_SYSTEM_PROMPT)
        ref_sys_prompt = compose_prompt(reflection_system_prompt, BASE_REFLECTION_SYSTEM_PROMPT)

        # Keep system prompts sticky while bounding context for speed/cost.
        # FixedFirstChatHistory ensures the first message (system) is never evicted.
        generation_history = FixedFirstChatHistory(
            [
                build_prompt_structure(prompt=gen_sys_prompt, role="system"),
                build_prompt_structure(prompt=user_msg, role="user"),
            ],
            total_length=3,  # system (fixed) + latest user/assistant turns
        )

        # Reflection history starts with just the reflection system message.
        reflection_history = FixedFirstChatHistory(
            [build_prompt_structure(prompt=ref_sys_prompt, role="system")],
            total_length=3,
        )

        final_generation: str = ""

        # -------------------------------------------------------------------
        # Iterative loop: generate -> reflect -> possibly stop/continue
        # -------------------------------------------------------------------
        for step in range(n_steps):
            if verbose > 0:
                fancy_step_tracker(step, n_steps)

            # 1) Generate content from the current generation history.
            final_generation = self.generate(generation_history, verbose=verbose)
            update_chat_history(generation_history, final_generation, "assistant")
            update_chat_history(reflection_history, final_generation, "user")

            # 2) Produce a critique of the generation.
            critique = self.reflect(reflection_history, verbose=verbose)

            # 3) Early stop if reflection deems the content satisfactory.
            if "<OK>" in critique:
                if verbose > 0:
                    print(
                        Fore.RED,
                        "\n\nStop Sequence found. Stopping the reflection loop ... \n\n",
                    )
                break

            # 4) Feed the critique back into the generation loop as the next user turn.
            update_chat_history(generation_history, critique, "user")
            update_chat_history(reflection_history, critique, "assistant")

        return final_generation
