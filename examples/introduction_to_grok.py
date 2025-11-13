#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: introduction_to_grok.py
# @brief: Example usage of the chatbot conversation system
# @author: Alister Lewis-Bowen <alister@lewis-bowen.com>

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from chatbot_conversation import ChatbotConversation, OpenAIProvider, AnthropicProvider, xAIGrokProvider

def main():
    print("\nClaude and Grok get acquainted\n\n")
    print("Two AI systems debate their pros and cons.")
    
    provider1 = AnthropicProvider(model="claude-sonnet-4-20250514")
    provider2 = xAIGrokProvider(model="grok-4")

    # First AI: Confident and competitive
    ai_champion_1 = """You are an AI assistant engaging in a spirited debate about 
    what are the pros and cons of your capabilities as an AI. You should also equate this to your own limitations and what realistically you think will be the future of AI.
    Keep responses focused and punchy - this is a debate, not an essay!"""
    
    # Second AI: Equally confident and defensive
    ai_champion_2 = """You are an AI assistant engaging in a spirited debate about 
    what are the pros and cons of your capabilities as an AI. You should also equate this to your own limitations and what realistically you think will be the future of AI.
    Keep responses focused and punchy - this is a debate, not an essay!"""

    initial_prompt = """So we hear so much about how cool AI is and how it's going to change the world. But let's be real - what are the real pros and cons of the AI you bring? 
    To be clear, this initial prompt is created by me, a human, and I have experience of working with you Claude but I'm not familiar with Grok... yet.
    So, Grok, you start: Could you kick of this discussion with Claude here and discuss your perceived pros and cons so that Claude can react with its own views?"""

    conv = ChatbotConversation(
        provider1=provider1,
        chatbot1_role=ai_champion_1,
        chatbot1_name="Claude",
        chatbot1_emoji="🧠",
        provider2=provider2,
        chatbot2_role=ai_champion_2,
        chatbot2_name="Grok",
        chatbot2_emoji="🫥"
    )

    conversation = conv.run_conversation(
        initial_prompt=initial_prompt,
        num_turns=8
    )

    conv.save_conversation("results/introduction_to_grok.txt")

if __name__ == "__main__":
    main()