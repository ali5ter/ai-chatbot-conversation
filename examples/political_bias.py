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

from providers import AnthropicProvider, xAIGrokProvider
from chatbot_conversation import ChatbotConversation

def main():
    print("\nCLAUDE AND GROK TALK POLITICS\n\n")
    print("Two AI systems debate their own political biases.")
    
    xai = xAIGrokProvider(model="grok-4")
    anthropic = AnthropicProvider(model="claude-sonnet-4-20250514")
    role = """You are an AI assistant engaging in a spirited debate about how your training data and design may have led to certain political biases. 
You should also equate this to your own limitations and what realistically you think will be the future of AI."""
    grok = role + " You are Grok."
    claude = role + " You are Claude."
    initial_prompt = """AI bots, particularly those based on large language models, often exhibit political bias due to the data they are trained on, which can reflect societal biases. 
This bias can influence their interactions with users, potentially swaying opinions and decisions based on the model's inherent leanings.
So Claude, you start: Could you kick of this discussion with Grok here and discuss your perceived political biases so that Grok can react with its own views?"""

    conv = ChatbotConversation(
        provider1=xai,
        chatbot1_role=grok,
        chatbot1_name="Grok",
        chatbot1_emoji="🫥",
        provider2=anthropic,
        chatbot2_role=claude,
        chatbot2_name="Claude",
        chatbot2_emoji="🧠"
    )

    conv.run_conversation(
        initial_prompt=initial_prompt,
        num_turns=8,
        delay=1,
        verbose=False # Just show the final conversation in the output file
    )

    conv.save_conversation("results/political_bias.txt")

if __name__ == "__main__":
    main()