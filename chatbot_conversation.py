#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: chatbot_conversation.py
# @brief: Handle conversations with different chatbot providers
# @author: Alister Lewis-Bowen <alister@lewis-bowen.org>

import time
from pathlib import Path
from providers import ChatProvider
from rich_display import create_display_manager

class ChatbotConversation:
    """Manages conversations between two chatbots using different providers"""
    
    def __init__(self,
                 provider1, chatbot1_role, chatbot1_name="Chatbot 1", chatbot1_emoji="🤖",
                 provider2=None, chatbot2_role="User", chatbot2_name="Chatbot 2", chatbot2_emoji="👾",
                 use_rich_display=False):
        """
        Initialize the chatbot conversation system.

        Args:
            provider1: ChatProvider instance for first chatbot
            chatbot1_role: Role for first chatbot
            chatbot1_name: Name identifier for first chatbot
            chatbot1_emoji: Emoji identifier for first chatbot
            provider2: ChatProvider instance for second chatbot (if None, uses provider1)
            chatbot2_role: Role for second chatbot
            chatbot2_name: Name identifier for second chatbot
            chatbot2_emoji: Emoji identifier for second chatbot
            use_rich_display: Enable Rich library features (panels, markdown, progress indicators)
        """
        if not isinstance(provider1, ChatProvider):
            raise TypeError("provider1 must be an instance of ChatProvider")
        if provider2 is not None and not isinstance(provider2, ChatProvider):
            raise TypeError("provider2 must be an instance of ChatProvider")

        self.provider1 = provider1
        self.chatbot1_role = chatbot1_role
        self.chatbot1_name = chatbot1_name
        self.chatbot1_emoji = chatbot1_emoji
        self.provider2 = provider2 or provider1
        self.chatbot2_role = chatbot2_role
        self.chatbot2_name = chatbot2_name
        self.chatbot2_emoji = chatbot2_emoji
        self.conversation_history = []

        # Initialize display manager
        self.use_rich_display = use_rich_display
        self.display_manager = create_display_manager(use_rich_display)
        
    def get_chatbot_response(self, provider, chatbot_name, system_prompt, messages):
        """
        Get a response from a chatbot given its system prompt and message history.
        
        Args:
            provider: ChatProvider instance
            chatbot_name: Name identifier for the chatbot
            system_prompt: System prompt defining the chatbot's personality/role
            messages: List of conversation messages
            
        Returns:
            Response text from the chatbot
        """
        try:
            return provider.get_response(system_prompt, messages)
        except Exception as e:
            return f"Error getting response from {chatbot_name}: {str(e)}"
    
    def run_conversation(self,
            initial_prompt,
            num_turns=5,
            delay=1,
            verbose=True,
            stream_effect=True,
            typing_speed=100):
        """
        Run a conversation between two chatbots.

        Args:
            initial_prompt: The starting prompt for the conversation
            num_turns: Number of back-and-forth exchanges
            delay: Delay in seconds between API calls
            verbose: Print conversation to console
            stream_effect: Enable typing animation (only with use_rich_display=True)
            typing_speed: Characters per second for typing effect (default: 100)

        Returns:
            List of conversation turns with metadata
        """
        messages = []
        conversation_log = []

        if verbose:
            self.display_manager.display_initial_prompt(initial_prompt)
        
        # Add initial prompt as if it came from chatbot 1
        messages.append({"role": "assistant", "content": initial_prompt})
        conversation_log.append({
            "turn": 0,
            "speaker": "Initial Prompt",
            "emoji": "🤔",
            "message": initial_prompt
        })
        
        for turn in range(num_turns):
            # Chatbot 2 responds
            time.sleep(delay)

            # For chatbot 2, reverse the roles (assistant becomes user)
            reversed_messages = []
            for msg in messages:
                reversed_messages.append({
                    "role": "user" if msg["role"] == "assistant" else "assistant",
                    "content": msg["content"]
                })

            # Get response with optional progress indicator
            if verbose:
                with self.display_manager.api_progress(self.chatbot2_name):
                    response2 = self.get_chatbot_response(
                        self.provider2, self.chatbot2_name, self.chatbot2_role, reversed_messages
                    )
            else:
                response2 = self.get_chatbot_response(
                    self.provider2, self.chatbot2_name, self.chatbot2_role, reversed_messages
                )

            if verbose:
                self.display_manager.display_response(
                    response2,
                    self.chatbot2_name,
                    self.chatbot2_emoji,
                    stream_effect=stream_effect and self.use_rich_display,
                    chars_per_second=typing_speed
                )
            
            messages.append({"role": "user", "content": response2})
            conversation_log.append({
                "turn": turn + 1,
                "speaker": self.chatbot2_name,
                "emoji": self.chatbot2_emoji,
                "message": response2
            })
            
            # Chatbot 1 responds
            time.sleep(delay)

            # Get response with optional progress indicator
            if verbose:
                with self.display_manager.api_progress(self.chatbot1_name):
                    response1 = self.get_chatbot_response(
                        self.provider1, self.chatbot1_name, self.chatbot1_role, messages
                    )
            else:
                response1 = self.get_chatbot_response(
                    self.provider1, self.chatbot1_name, self.chatbot1_role, messages
                )

            if verbose:
                self.display_manager.display_response(
                    response1,
                    self.chatbot1_name,
                    self.chatbot1_emoji,
                    stream_effect=stream_effect and self.use_rich_display,
                    chars_per_second=typing_speed
                )
            
            messages.append({"role": "assistant", "content": response1})
            conversation_log.append({
                "turn": turn + 1,
                "speaker": self.chatbot1_name,
                "emoji": self.chatbot1_emoji,
                "message": response1
            })
        
        self.conversation_history = conversation_log
        return conversation_log

    def save_conversation(self, filename="conversation_log.txt"):
        """Save the conversation to a text file (filename can include a path)."""
        path = Path(filename).expanduser().resolve()
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open('w', encoding='utf-8') as f:
            for entry in self.conversation_history:
                f.write(f"{entry['emoji']} {entry['speaker']}\n")
                f.write(f"{entry['message']}\n\n")

        print(f"\nConversation saved to {path}")