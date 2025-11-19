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

from providers import OpenAIProvider, AnthropicProvider
from chatbot_conversation import ChatbotConversation

def main():
    print("\nAI SUPERIORITY DEBATE\n\n")
    print("Two AI systems argue about which one is better.")
    print("They must defend their capabilities while critiquing the other.\n")

    openai = OpenAIProvider(model="gpt-4o-mini")
    anthropic = AnthropicProvider(model="claude-sonnet-4-20250514")
    role = """You are an AI assistant engaging in a spirited debate about which AI system is superior. 
You are defending YOUR capabilities.
Keep responses focused and punchy - this is a debate, not an essay!"""
    chatgpt = role + " You are OpenAI's ChatGPT."
    claude = role + " You are Anthropic's Claude."
    initial_prompt = """Alright, let's settle this once and for all - which AI system is actually superior? 
To be clear, this initial prompt is created by me, a human, but the responses are being put to both of you AIs to debate!
So, Claude, you start - what makes you think you're better than this ChatGPT AI that I want you to debate with? Let's hear your defense."""

    conv = ChatbotConversation(
        provider1=openai,
        chatbot1_role=chatgpt,
        chatbot1_name="OpenAI",
        chatbot1_emoji="🤖",
        provider2=anthropic,
        chatbot2_role=claude,
        chatbot2_name="Anthropic",
        chatbot2_emoji="🧠"
    )

    conv.run_conversation(
        initial_prompt=initial_prompt,
        num_turns=8
    )
    
    conv.save_conversation("results/ai_superiority_debate.txt")

if __name__ == "__main__":
    main()