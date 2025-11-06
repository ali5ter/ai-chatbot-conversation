#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: basic_conversation.py
# @brief: Example usage of the chatbot conversation system
# @author: Alister Lewis-Bowen <alister@lewis-bowen.org>

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from chatbot_conversation import (
    ChatbotConversation,
    OpenAIProvider,
    AnthropicProvider,
    OllamaProvider
)

def main():
    # Choose your provider(s):
    
    # Option 1: OpenAI (both chatbots)
    # provider1 = OpenAIProvider(model="gpt-4o-mini")
    # provider2 = OpenAIProvider(model="gpt-4o-mini")
    
    # Option 2: Anthropic Claude (both chatbots)
    # provider1 = AnthropicProvider(model="claude-sonnet-4-20250514")
    # provider2 = AnthropicProvider(model="claude-sonnet-4-20250514")
    
    # Option 3: Mix providers (e.g., OpenAI vs Claude)
    provider1 = OpenAIProvider(model="gpt-4o-mini")
    provider2 = AnthropicProvider(model="claude-sonnet-4-20250514")
    
    # Option 4: Local models with Ollama
    # provider1 = OllamaProvider(model="llama2")
    # provider2 = OllamaProvider(model="mistral")
    
    # Define roles and personalities for the chatbots
    policy_expert = """You are an AI policy expert with a focus on practical implementation. 
    You think about concrete tools, specific policy language, and real-world applications. 
    You like to provide detailed examples and actionable recommendations."""
    
    ethics_researcher = """You are an AI ethics and detection researcher who thinks critically 
    about AI detection methods and their limitations. You enjoy exploring edge cases, 
    potential issues, and philosophical implications while also being practical."""
    
    # The initial prompt
    initial_prompt = """If you were able to detect if some text was AI generated, what ways 
    would you do this and how might this provide the basis for some AI usage policy that a 
    non-profit might use? Brainstorm specific tools readily available to employees to use and 
    specific content to include in a policy... discuss."""

    # Initialize the conversation system
    conv = ChatbotConversation(
        provider1=provider1,
        chatbot1_role=policy_expert,
        chatbot1_name="Policy Expert",
        chatbot1_emoji="📋",
        provider2=provider2,
        chatbot2_role=ethics_researcher,
        chatbot2_name="Ethics Researcher",
        chatbot2_emoji="🔬"
    )
    
    # Run the conversation for 3 turns (6 total messages)
    conversation = conv.run_conversation(
        initial_prompt=initial_prompt,
        num_turns=3
    )
    
    # Save the conversation
    conv.save_conversation("results/ai_policy_discussion.txt")

if __name__ == "__main__":
    main()
