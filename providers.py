#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: providers.py
# @brief: API provider implementations for chatbot conversations
# @author: Alister Lewis-Bowen <alister@lewis-bowen.org>

import os
from abc import ABC, abstractmethod

# Try to load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, will use system environment variables

class ChatProvider(ABC):
    """Base class for different API providers"""
    
    def __init__(self):
        """Initialize provider with default values from environment variables"""
        # Get defaults from environment variables or use hardcoded defaults
        self.default_temperature = float(os.environ.get("DEFAULT_TEMPERATURE", "0.7"))
        self.default_max_tokens = int(os.environ.get("DEFAULT_MAX_TOKENS", "500"))

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
    
    def __init__(self, api_key=None, model="gpt-4o-mini", temperature=None, max_tokens=None):
        super().__init__()
        
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
        
        # Provider-specific defaults from environment or use base class defaults
        self.default_temperature = temperature if temperature is not None else float(
            os.environ.get("OPENAI_TEMPERATURE", self.default_temperature)
        )
        self.default_max_tokens = max_tokens if max_tokens is not None else int(
            os.environ.get("OPENAI_MAX_TOKENS", self.default_max_tokens)
        )
        
        print(f"OpenAI Provider initialized with model: {model}")
        print(f"  Default temperature: {self.default_temperature}")
        print(f"  Default max_tokens: {self.default_max_tokens}")
    
    def get_response(self, system_prompt, messages, temperature=None, max_tokens=None):
        # Use provided values or fall back to provider defaults
        temp = temperature if temperature is not None else self.default_temperature
        tokens = max_tokens if max_tokens is not None else self.default_max_tokens
        
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        response = self.client.chat.completions.create(
            model=self.model,
            messages=full_messages,
            temperature=temp,
            max_tokens=tokens
        )
        return response.choices[0].message.content


class AnthropicProvider(ChatProvider):
    """Anthropic Claude API provider"""
    """Default Claude System Prompt: https://docs.claude.com/en/release-notes/system-prompts"""

    """
    What is a System Prompt? 
    
    The set of overarching instructions that the model sees before the start of
    any conversation. These instructions help define the model's behavior, personality,
    and guidelines for generating responses. System prompts are crucial for tailoring
    the model's output to specific use cases or desired interaction styles.
    """
    
    def __init__(self, api_key=None, model="claude-sonnet-4-20250514", temperature=None, max_tokens=None):
        super().__init__()

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

        # Provider-specific defaults from environment or use base class defaults
        self.default_temperature = temperature if temperature is not None else float(
            os.environ.get("ANTHROPIC_TEMPERATURE", self.default_temperature)
        )
        self.default_max_tokens = max_tokens if max_tokens is not None else int(
            os.environ.get("ANTHROPIC_MAX_TOKENS", self.default_max_tokens)
        )
        
        print(f"Anthropic Provider initialized with model: {model}")
        print(f"  Default temperature: {self.default_temperature}")
        print(f"  Default max_tokens: {self.default_max_tokens}")
    
    def get_response(self, system_prompt, messages, temperature=None, max_tokens=None):
        # Use provided values or fall back to provider defaults
        temp = temperature if temperature is not None else self.default_temperature
        tokens = max_tokens if max_tokens is not None else self.default_max_tokens
        
        # Convert messages to Anthropic format
        anthropic_messages = []
        for msg in messages:
            anthropic_messages.append({
                "role": msg["role"] if msg["role"] != "assistant" else "assistant",
                "content": msg["content"]
            })
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=tokens,
            temperature=temp,
            system=system_prompt,
            messages=anthropic_messages
        )
        return response.content[0].text


class OllamaProvider(ChatProvider):
    """Ollama provider for local models"""
    """Default Llama System Prompt: https://www.llama.com/docs/model-cards-and-prompt-formats/llama4/"""

    """
    What is a System Prompt? 
    
    The set of overarching instructions that the model sees before the start of
    any conversation. These instructions help define the model's behavior, personality,
    and guidelines for generating responses. System prompts are crucial for tailoring
    the model's output to specific use cases or desired interaction styles.
    """
    
    def __init__(self, model="llama2", base_url="http://localhost:11434", temperature=None, max_tokens=None):
        super().__init__()

        try:
            import requests
        except ImportError:
            raise ImportError("Requests package not installed. Run: pip install requests")
        
        self.model = model
        self.base_url = base_url
        self.session = requests.Session()

        # Provider-specific defaults from environment or use base class defaults
        self.default_temperature = temperature if temperature is not None else float(
            os.environ.get("OLLAMA_TEMPERATURE", self.default_temperature)
        )
        self.default_max_tokens = max_tokens if max_tokens is not None else int(
            os.environ.get("OLLAMA_MAX_TOKENS", self.default_max_tokens)
        )
        
        print(f"Ollama Provider initialized with model: {model}")
        print(f"  Default temperature: {self.default_temperature}")
        print(f"  Default max_tokens: {self.default_max_tokens}")
    
    def get_response(self, system_prompt, messages, temperature=None, max_tokens=None):
        import requests
        
        # Use provided values or fall back to provider defaults
        temp = temperature if temperature is not None else self.default_temperature
        tokens = max_tokens if max_tokens is not None else self.default_max_tokens

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
                    "temperature": temp,
                    "num_predict": tokens
                }
            }
        )
        return response.json()["response"]


class xAIGrokProvider(ChatProvider):
    """xAI Grok API provider"""
    """Default Grok System Prompt: hhttps://github.com/xai-org/grok-prompts/blob/main/grok4_system_turn_prompt_v8.j2"""

    """
    What is a System Prompt? 
    
    The set of overarching instructions that the model sees before the start of
    any conversation. These instructions help define the model's behavior, personality,
    and guidelines for generating responses. System prompts are crucial for tailoring
    the model's output to specific use cases or desired interaction styles.
    """
    
    def __init__(self, api_key=None, model="grok-4", base_url="https://api.x.ai/v1", temperature=None, max_tokens=None):
        super().__init__()

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
        
        # Provider-specific defaults from environment or use base class defaults
        self.default_temperature = temperature if temperature is not None else float(
            os.environ.get("XAI_TEMPERATURE", self.default_temperature)
        )
        self.default_max_tokens = max_tokens if max_tokens is not None else int(
            os.environ.get("XAI_MAX_TOKENS", self.default_max_tokens)
        )
        
        print(f"Grok Provider initialized with model: {model}")
        print(f"  Default temperature: {self.default_temperature}")
        print(f"  Default max_tokens: {self.default_max_tokens}")

    def get_response(self, system_prompt, messages, temperature=None, max_tokens=None):

        # Use provided values or fall back to provider defaults
        temp = temperature if temperature is not None else self.default_temperature
        tokens = max_tokens if max_tokens is not None else self.default_max_tokens

        full_messages = [{"role": "system", "content": system_prompt}] + messages
        response = self.client.chat.completions.create(
            model=self.model,
            messages=full_messages,
            temperature=temp,
            max_tokens=tokens
        )
        return response.choices[0].message.content

class GoogleProvider(ChatProvider):
    """Google Gemini API provider"""
    
    def __init__(self, api_key=None, model="gemini-2.5-flash", temperature=None, max_tokens=None):
        super().__init__()

        try:
            import google.generativeai as genai
            self.genai = genai
        except ImportError:
            raise ImportError("Google Generative AI package not installed. Run: pip install google-generativeai")
        
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Gemini API key not found. Set GEMINI_API_KEY environment variable or pass api_key parameter.\n"
                "Get your API key at: https://makersuite.google.com/app/apikey"
            )
        
        # Configure the API
        self.genai.configure(api_key=self.api_key)

        # Use base model name without 'models/' prefix
        # The API will handle the proper formatting
        if model.startswith('models/'):
            self.model_name = model.replace('models/', '')
        else:
            self.model_name = model
        
        # Provider-specific defaults from environment or use base class defaults
        self.default_temperature = temperature if temperature is not None else float(
            os.environ.get("GEMINI_TEMPERATURE", self.default_temperature)
        )
        self.default_max_tokens = max_tokens if max_tokens is not None else int(
            os.environ.get("GEMINI_MAX_TOKENS", self.default_max_tokens)
        )
        
        print(f"Gemini Provider initialized with model: {model}")
        print(f"  Default temperature: {self.default_temperature}")
        print(f"  Default max_tokens: {self.default_max_tokens}")
    
    def get_response(self, system_prompt, messages, temperature=None, max_tokens=None):
        # Use provided values or fall back to provider defaults
        temp = temperature if temperature is not None else self.default_temperature
        tokens = max_tokens if max_tokens is not None else self.default_max_tokens
        
        # Configure generation settings with safety settings
        generation_config = {
            "temperature": temp,
            "max_output_tokens": tokens,
        }
        
        # Relax safety settings to reduce blocking
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
        ]
        
        # Create model with system instruction
        model = self.genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=generation_config,
            safety_settings=safety_settings,
            system_instruction=system_prompt
        )
        
        # Convert messages to Gemini format
        # Gemini expects history as a list of Content objects
        history = []
        for msg in messages[:-1]:  # All but the last message
            role = "user" if msg["role"] == "user" else "model"
            history.append({
                "role": role,
                "parts": [msg["content"]]
            })
        
        # Start chat with history
        chat = model.start_chat(history=history)
        
        # Send the last message
        last_message = messages[-1]["content"] if messages else ""
        response = chat.send_message(last_message)
        
        # Handle different response scenarios
        try:
            # Try to get text normally
            return response.text
        except ValueError as e:
            # Response was blocked or empty
            if hasattr(response, 'prompt_feedback'):
                # Check if prompt was blocked
                feedback = response.prompt_feedback
                if hasattr(feedback, 'block_reason'):
                    return f"[Response blocked by safety filter: {feedback.block_reason}]"
            
            # Check candidates for finish reason
            if response.candidates:
                candidate = response.candidates[0]
                finish_reason = candidate.finish_reason
                
                # Map finish reasons to user-friendly messages
                reasons = {
                    1: "STOP - completed normally",
                    2: "SAFETY - content filtered",
                    3: "RECITATION - too similar to training data",
                    4: "MAX_TOKENS - reached token limit",
                    5: "OTHER - unknown reason"
                }
                
                reason_text = reasons.get(finish_reason, f"Unknown reason: {finish_reason}")
                
                # Try to get partial content if available
                if hasattr(candidate, 'content') and candidate.content.parts:
                    try:
                        partial = "".join([part.text for part in candidate.content.parts if hasattr(part, 'text')])
                        if partial:
                            return f"{partial}\n\n[Response may be incomplete - finish reason: {reason_text}]"
                    except:
                        pass
                
                return f"[Response blocked - {reason_text}]"
            
            # Fallback error message
            return f"[Error generating response: {str(e)}]"