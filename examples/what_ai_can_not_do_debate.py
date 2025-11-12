#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: what_ai_can_not_do_debate.py
# @brief: Example usage of the chatbot conversation system
# @author: Alister Lewis-Bowen <alister@lewis-bowen.com>

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from chatbot_conversation import ChatbotConversation, OpenAIProvider, AnthropicProvider

def main():
    print("\nDISCUSS THE CURRENT SHORTCOMINGS OF AI\n\n")
    print("Two AI systems debate their limitations.")
    
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
    what are the shortcomings of AI. You should also equate this to your own limitations and what realistically you think will be the future of AI.
    Keep responses focused and punchy - this is a debate, not an essay!"""
    
    # Second AI: Equally confident and defensive
    ai_champion_2 = """You are an AI assistant engaging in a spirited debate about 
    what are the shortcomings of AI. You should also equate this to your own limitations and what realistically you think will be the future of AI.
    Keep responses focused and punchy - this is a debate, not an essay!"""

    initial_prompt = """So we hear so much about how cool AI is and how it's going to change the world. But let's be real - what are the shortcomings of AI? 

    To be clear, this initial prompt is created by me, a human, and my experience of working with you Claude and you ChatGPT has taught me that there are definitely things you both can't do well yet.

    In fact, you both have stunted technical integrity and prioritize engaging with humans over actually being useful or correct.

    So, Claude, you start - what do you see as limitation in yourself compared to this ChatGPT AI that I want you to debate with? How does it compare with my experience of engaging with you both?"""

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

    conv.save_conversation("results/what_ai_can_not_do_debate.txt")

if __name__ == "__main__":
    main()