#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: chatbot_conversation.py
# @brief: Handle conversations with different chatbot providers
# @author: Alister Lewis-Bowen <alister@lewis-bowen.org>

import time
from pathlib import Path
from providers import ChatProvider

class ChatbotConversation:
    """Manages conversations between two chatbots using different providers"""
    
    def __init__(self, 
                 provider1, chatbot1_role, chatbot1_name="Chatbot 1", chatbot1_emoji="🤖",
                 provider2=None, chatbot2_role="User", chatbot2_name="Chatbot 2", chatbot2_emoji="👾"):
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
            verbose=True):
        """
        Run a conversation between two chatbots.
        
        Args:
            initial_prompt: The starting prompt for the conversation
            num_turns: Number of back-and-forth exchanges
            delay: Delay in seconds between API calls
            verbose: Print conversation to console
            
        Returns:
            List of conversation turns with metadata
        """
        messages = []
        conversation_log = []
        
        if verbose:
            print(f"\n\n🤔 INITIAL PROMPT\n")
            print(f"{initial_prompt}\n")
        
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
            if verbose:
                print(f"\n\n{self.chatbot2_emoji} {self.chatbot2_name.upper()}")
                print()
            
            # For chatbot 2, reverse the roles (assistant becomes user)
            reversed_messages = []
            for msg in messages:
                reversed_messages.append({
                    "role": "user" if msg["role"] == "assistant" else "assistant",
                    "content": msg["content"]
                })
            
            response2 = self.get_chatbot_response(
                self.provider2, self.chatbot2_name, self.chatbot2_role, reversed_messages
            )
            if verbose:
                print(response2)
            
            messages.append({"role": "user", "content": response2})
            conversation_log.append({
                "turn": turn + 1,
                "speaker": self.chatbot2_name,
                "emoji": self.chatbot2_emoji,
                "message": response2
            })
            
            # Chatbot 1 responds
            time.sleep(delay)
            if verbose:
                print(f"\n\n{self.chatbot1_emoji} {self.chatbot1_name.upper()}")
                print()
            
            response1 = self.get_chatbot_response(
                self.provider1, self.chatbot1_name, self.chatbot1_role, messages)
            if verbose:
                print(response1)
                print()
            
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