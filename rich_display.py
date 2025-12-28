#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: rich_display.py
# @brief: Rich library integration for enhanced console output
# @author: Alister Lewis-Bowen <alister@lewis-bowen.org>

from contextlib import contextmanager
import time
from typing import Optional


class RichDisplayManager:
    """Manages Rich-enhanced console output for chatbot conversations"""

    def __init__(self):
        from rich.console import Console
        self.console = Console()

    @contextmanager
    def api_progress(self, chatbot_name: str):
        """
        Context manager for displaying progress during blocking API calls.
        Uses Rich spinner in a separate context.

        Usage:
            with display_manager.api_progress("ChatBot 1"):
                response = provider.get_response(...)
        """
        from rich.progress import Progress, SpinnerColumn, TextColumn

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True  # Disappears when done
        ) as progress:
            progress.add_task(
                description=f"Waiting for {chatbot_name} response...",
                total=None  # Indeterminate progress
            )
            yield

    def display_initial_prompt(self, prompt: str, emoji: str = "🤔"):
        """Display the initial prompt with Rich formatting"""
        from rich.panel import Panel
        from rich.markdown import Markdown

        title = f"{emoji} INITIAL PROMPT"
        panel = Panel(
            Markdown(prompt),
            title=title,
            border_style="bright_cyan",
            padding=(1, 2)
        )
        self.console.print()
        self.console.print(panel)

    def display_response(self,
                        response: str,
                        chatbot_name: str,
                        emoji: str,
                        stream_effect: bool = True,
                        chars_per_second: int = 100):
        """
        Display chatbot response with Rich panel and optional streaming effect.

        Args:
            response: The complete response text
            chatbot_name: Name of the chatbot
            emoji: Emoji identifier
            stream_effect: Whether to simulate typing animation
            chars_per_second: Speed of typing effect (characters per second)
        """
        title = f"{emoji} {chatbot_name.upper()}"

        if stream_effect:
            # Simulate streaming with Live display
            self._display_with_stream_effect(
                response, title, chars_per_second
            )
        else:
            # Display complete response immediately
            from rich.panel import Panel
            from rich.markdown import Markdown

            panel = Panel(
                Markdown(response),
                title=title,
                border_style="blue",
                padding=(1, 2)
            )
            self.console.print()
            self.console.print(panel)

    def _display_with_stream_effect(self,
                                    response: str,
                                    title: str,
                                    chars_per_second: int):
        """
        Internal method to display text with typing animation effect.
        Works with blocking API calls by animating the complete response.
        """
        from rich.live import Live

        self.console.print()

        # Create initial empty panel
        accumulated_text = ""

        with Live(
            self._create_panel(accumulated_text, title),
            console=self.console,
            refresh_per_second=20
        ) as live:
            # Animate the complete response character by character
            for char in response:
                accumulated_text += char
                live.update(self._create_panel(accumulated_text, title))

                # Sleep based on chars_per_second
                # Adjust for faster rendering of whitespace
                if char in [' ', '\n', '\t']:
                    time.sleep(0.01)  # Fast for whitespace
                else:
                    time.sleep(1.0 / chars_per_second)

    def _create_panel(self, text: str, title: str):
        """Helper to create a panel with markdown content"""
        from rich.panel import Panel
        from rich.markdown import Markdown

        return Panel(
            Markdown(text) if text else "",
            title=title,
            border_style="blue",
            padding=(1, 2),
            height=None  # Allow panel to grow to fit content
        )


class SimpleDisplayManager:
    """Fallback display manager using simple print statements"""

    @contextmanager
    def api_progress(self, chatbot_name: str):
        """No-op progress indicator for simple mode"""
        yield

    def display_initial_prompt(self, prompt: str, emoji: str = "🤔"):
        """Display initial prompt with simple print"""
        print(f"\n\n{emoji} INITIAL PROMPT\n")
        print(f"{prompt}\n")

    def display_response(self,
                        response: str,
                        chatbot_name: str,
                        emoji: str,
                        stream_effect: bool = False,
                        chars_per_second: int = 100):
        """Display response with simple print"""
        print(f"\n\n{emoji} {chatbot_name.upper()}")
        print()
        print(response)


def create_display_manager(use_rich: bool = False):
    """
    Factory function to create appropriate display manager.

    Args:
        use_rich: Whether to use Rich display features

    Returns:
        RichDisplayManager or SimpleDisplayManager instance
    """
    if use_rich:
        try:
            return RichDisplayManager()
        except ImportError:
            print("Warning: Rich library not installed. Falling back to simple display.")
            print("Install with: pip install rich")
            return SimpleDisplayManager()
    return SimpleDisplayManager()
