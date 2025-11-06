#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: climate_policy_debate.py
# @brief: Example usage of the chatbot conversation system
# @author: Alister Lewis-Bowen <alister@lewis-bowen.com>

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from chatbot_conversation import ChatbotConversation, OpenAIProvider, AnthropicProvider

def main():
    print("\nAI SUPERIORITY DEBATE\n\n")
    print("Two AI systems argue about which one is better.")
    print("They must defend their capabilities while critiquing the other.\n")
    
    # For maximum entertainment, use DIFFERENT providers
    # Option 1: GPT vs GPT (same model arguing with itself)
    # provider1 = OpenAIProvider(model="gpt-4o-mini")
    # provider2 = OpenAIProvider(model="gpt-4o-mini")
    
    # Option 2: GPT vs Claude (most interesting - actual different models!)
    provider1 = OpenAIProvider(model="gpt-4o-mini")
    provider2 = AnthropicProvider(model="claude-sonnet-4-20250514")
    
    # Option 3: Different GPT versions
    # provider1 = OpenAIProvider(model="gpt-4o")
    # provider2 = OpenAIProvider(model="gpt-4o-mini")

    # First AI: Confident and competitive
    ai_champion_1 = """You are an AI assistant engaging in a spirited debate about 
    which AI system is superior. You are defending YOUR capabilities.
    Keep responses focused and punchy - this is a debate, not an essay!"""
    
    # Second AI: Equally confident and defensive
    ai_champion_2 = """You are an AI assistant engaging in a spirited debate about 
    which AI system is superior. You are defending YOUR capabilities.
    Keep responses focused and punchy - this is a debate, not an essay!"""
    
    initial_prompt = """Alright, let's settle this once and for all - which AI system is 
    actually superior? 

    To be clear, this initial prompt is created by me, a human, but the responses are being put to both of you AIs to debate!

    So, Claude, you start - what makes you think you're better than this ChatGPT AI that I want you to debate with? Let's hear your defense."""

    conv = ChatbotConversation(
        provider1=provider1,
        chatbot1_role=ai_champion_1,
        chatbot1_name="OpenAI",
        chatbot1_emoji="🤖",
        provider2=provider2,
        chatbot2_role=ai_champion_2,
        chatbot2_name="Anthropic",
        chatbot2_emoji="🧠"
    )

    conversation = conv.run_conversation(
        initial_prompt=initial_prompt,
        num_turns=8
    )
    
    conv.save_conversation("results/ai_superiority_debate.txt")

if __name__ == "__main__":
    main()