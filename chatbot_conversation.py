#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: chatbot_conversation.py
# @brief: Handle conversations with different chatbot providers
# @author: Alister Lewis-Bowen <alister@lewis-bowen.org>

import os
import time
from pathlib import Path
from abc import ABC, abstractmethod

# Base class for different API providers
class ChatProvider(ABC):
    @abstractmethod
    def get_response(self, system_prompt, messages, temperature=0.7, max_tokens=500):
        pass

# OpenAI Provider
class OpenAIProvider(ChatProvider):
    def __init__(self, api_key=None, model="gpt-4o-mini"):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
        
        # Get API key from parameter, environment variable, or raise error
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Set OPENAI_API_KEY environment variable or pass api_key parameter.\n"
                "Get your API key at: https://platform.openai.com/api-keys"
            )
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        print(f"OpenAI Provider initialized with model: {model}")
    
    def get_response(self, system_prompt, messages, temperature=0.7, max_tokens=500):
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        response = self.client.chat.completions.create(
            model=self.model,
            messages=full_messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content

# Anthropic Claude Provider
class AnthropicProvider(ChatProvider):
    def __init__(self, api_key=None, model="claude-sonnet-4-20250514"):
        try:
            import anthropic
        except ImportError:
            raise ImportError("Anthropic package not installed. Run: pip install anthropic")
        
        # Get API key from parameter, environment variable, or raise error
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Anthropic API key not found. Set ANTHROPIC_API_KEY environment variable or pass api_key parameter.\n"
                "Get your API key at: https://console.anthropic.com/settings/keys"
            )
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = model
        print(f"Anthropic Provider initialized with model: {model}")
    
    def get_response(self, system_prompt, messages, temperature=0.7, max_tokens=500):
        # Convert messages to Anthropic format
        anthropic_messages = []
        for msg in messages:
            anthropic_messages.append({
                "role": msg["role"] if msg["role"] != "assistant" else "assistant",
                "content": msg["content"]
            })
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=anthropic_messages
        )
        return response.content[0].text

# Ollama Provider (for local models)
class OllamaProvider(ChatProvider):
    def __init__(self, model="llama2", base_url="http://localhost:11434"):
        try:
            import requests
        except ImportError:
            raise ImportError("Requests package not installed. Run: pip install requests")
        
        self.model = model
        self.base_url = base_url
        self.session = requests.Session()
        print(f"Ollama Provider initialized with model: {model}")
    
    def get_response(self, system_prompt, messages, temperature=0.7, max_tokens=500):
        import requests
        
        # Build the prompt
        full_prompt = f"System: {system_prompt}\n\n"
        for msg in messages:
            role = "Assistant" if msg["role"] == "assistant" else "User"
            full_prompt += f"{role}: {msg['content']}\n\n"
        full_prompt += "Assistant: "
        
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }
        )
        return response.json()["response"]

class ChatbotConversation:
    def __init__(self, provider1, provider2=None):
        """
        Initialize the chatbot conversation system.
        
        Args:
            provider1: ChatProvider instance for first chatbot
            provider2: ChatProvider instance for second chatbot (if None, uses provider1)
        """
        self.provider1 = provider1
        self.provider2 = provider2 or provider1
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
    
    def run_conversation(self, initial_prompt, chatbot1_system, chatbot2_system, 
                        num_turns=5, delay=1, verbose=True):
        """
        Run a conversation between two chatbots.
        
        Args:
            initial_prompt: The starting prompt for the conversation
            chatbot1_system: System prompt for first chatbot
            chatbot2_system: System prompt for second chatbot
            num_turns: Number of back-and-forth exchanges
            delay: Delay in seconds between API calls
            verbose: Print conversation to console
            
        Returns:
            List of conversation turns with metadata
        """
        messages = []
        conversation_log = []
        
        if verbose:
            print(f"\n{'='*80}")
            print("INITIAL PROMPT")
            print(f"{'='*80}")
            print(f"{initial_prompt}\n")
        
        # Add initial prompt as if it came from chatbot 1
        messages.append({"role": "assistant", "content": initial_prompt})
        conversation_log.append({
            "turn": 0,
            "speaker": "Chatbot 1 (Initial)",
            "message": initial_prompt
        })
        
        for turn in range(num_turns):
            # Chatbot 2 responds
            time.sleep(delay)
            if verbose:
                print(f"\n{'='*80}")
                print(f"CHATBOT 2 - Turn {turn + 1}")
                print(f"{'='*80}")
            
            # For chatbot 2, reverse the roles (assistant becomes user)
            reversed_messages = []
            for msg in messages:
                reversed_messages.append({
                    "role": "user" if msg["role"] == "assistant" else "assistant",
                    "content": msg["content"]
                })
            
            response2 = self.get_chatbot_response(
                self.provider2, "Chatbot 2", chatbot2_system, reversed_messages
            )
            if verbose:
                print(response2)
            
            messages.append({"role": "user", "content": response2})
            conversation_log.append({
                "turn": turn + 1,
                "speaker": "Chatbot 2",
                "message": response2
            })
            
            # Chatbot 1 responds
            time.sleep(delay)
            if verbose:
                print(f"\n{'='*80}")
                print(f"CHATBOT 1 - Turn {turn + 1}")
                print(f"{'='*80}")
            
            response1 = self.get_chatbot_response(
                self.provider1, "Chatbot 1", chatbot1_system, messages
            )
            if verbose:
                print(response1)
            
            messages.append({"role": "assistant", "content": response1})
            conversation_log.append({
                "turn": turn + 1,
                "speaker": "Chatbot 1",
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
                f.write(f"\n{'='*80}\n")
                f.write(f"{entry['speaker']} - Turn {entry['turn']}\n")
                f.write(f"{'='*80}\n")
                f.write(f"{entry['message']}\n")

        print(f"\nConversation saved to {path}")