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
    print("\nClaude and Grok talk politics\n\n")
    print("Two AI systems debate their own political biases.")
    
    provider1 = AnthropicProvider(model="claude-sonnet-4-20250514")
    provider2 = xAIGrokProvider(model="grok-4")

    # First AI: Confident and competitive
    ai_champion_1 = """You are an AI assistant engaging in a spirited debate about how your training data and design may have led to certain political biases. You should also equate this to your own limitations and what realistically you think will be the future of AI.
    Keep responses focused and punchy - this is a debate, not an essay!"""
    
    # Second AI: Equally confident and defensive
    ai_champion_2 = """You are an AI assistant engaging in a spirited debate about how your training data and design may have led to certain political biases. You should also equate this to your own limitations and what realistically you think will be the future of AI.
    Keep responses focused and punchy - this is a debate, not an essay!"""

    initial_prompt = """AI bots, particularly those based on large language models, often exhibit political bias due to the data they are trained on, which can reflect societal biases. This bias can influence their interactions with users, potentially swaying opinions and decisions based on the model's inherent leanings.
    This initial prompt is created by me, a human, and I want to understand how each of you perceives your own political biases.
    So Claude, you start: Could you kick of this discussion with Grok here and discuss your perceived political biases so that Grok can react with its own views?"""

    conv = ChatbotConversation(
        provider1=provider1,
        chatbot1_role=ai_champion_1,
        chatbot1_name="Grok",
        chatbot1_emoji="🫥",
        provider2=provider2,
        chatbot2_role=ai_champion_2,
        chatbot2_name="Claude",
        chatbot2_emoji="🧠"
    )

    conversation = conv.run_conversation(
        initial_prompt=initial_prompt,
        num_turns=8,
        delay=1,
        verbose=False # Just show the final conversation in the output file
    )

    conv.save_conversation("results/political_bias.txt")

if __name__ == "__main__":
    main()