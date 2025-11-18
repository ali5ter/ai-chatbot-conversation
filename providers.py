#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: providers.py
# @brief: API provider implementations for chatbot conversations
# @author: Alister Lewis-Bowen <alister@lewis-bowen.org>

import os
from abc import ABC, abstractmethod


class ChatProvider(ABC):
    """Base class for different API providers"""
    
    @abstractmethod
    def get_response(self, system_prompt, messages, temperature=0.7, max_tokens=500):
        """
        Get a response from the chat provider.
        
        Args:
            system_prompt: System prompt defining the chatbot's personality/role
            messages: List of conversation messages in OpenAI format
            temperature: Sampling temperature for response generation
            max_tokens: Maximum tokens in response
            
        Returns:
            Response text from the provider
        """
        pass


class OpenAIProvider(ChatProvider):
    """OpenAI API provider for GPT models"""
    
    def __init__(self, api_key=None, model="gpt-4o-mini"):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
        
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


class AnthropicProvider(ChatProvider):
    """Anthropic Claude API provider"""
    """Claude System Prompt: https://docs.claude.com/en/release-notes/system-prompts"""

    """
    What is a System Prompt? 
    
    The set of overarching instructions that the model sees before the start of
    any conversation. These instructions help define the model's behavior, personality,
    and guidelines for generating responses. System prompts are crucial for tailoring
    the model's output to specific use cases or desired interaction styles.
    """
    
    def __init__(self, api_key=None, model="claude-sonnet-4-20250514"):
        try:
            import anthropic
        except ImportError:
            raise ImportError("Anthropic package not installed. Run: pip install anthropic")
        
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


class OllamaProvider(ChatProvider):
    """Ollama provider for local models"""
    """System Prompt: https://www.llama.com/docs/model-cards-and-prompt-formats/llama4/"""

    """
    What is a System Prompt? 
    
    The set of overarching instructions that the model sees before the start of
    any conversation. These instructions help define the model's behavior, personality,
    and guidelines for generating responses. System prompts are crucial for tailoring
    the model's output to specific use cases or desired interaction styles.
    """
    
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


class xAIGrokProvider(ChatProvider):
    """xAI Grok API provider"""
    """System Prompt: hhttps://github.com/xai-org/grok-prompts/blob/main/grok4_system_turn_prompt_v8.j2"""

    """
    What is a System Prompt? 
    
    The set of overarching instructions that the model sees before the start of
    any conversation. These instructions help define the model's behavior, personality,
    and guidelines for generating responses. System prompts are crucial for tailoring
    the model's output to specific use cases or desired interaction styles.
    """
    
    def __init__(self, api_key=None, model="grok-4", base_url="https://api.x.ai/v1"):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")

        self.api_key = api_key or os.environ.get("XAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "xAI API key not found. Set XAI_API_KEY or pass api_key.\n"
                "Create a key at: https://console.x.ai/"
            )
        
        self.client = OpenAI(api_key=self.api_key, base_url=base_url)
        self.model = model
        print(f"Grok Provider initialized with model: {model}")

    def get_response(self, system_prompt, messages, temperature=0.7, max_tokens=500):
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        response = self.client.chat.completions.create(
            model=self.model,
            messages=full_messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content