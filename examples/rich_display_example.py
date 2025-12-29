#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: rich_display_example.py
# @brief: Example demonstrating Rich library features for enhanced console display
# @author: Alister Lewis-Bowen <alister@lewis-bowen.org>

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load .env automatically to get environment variables for API keys
from dotenv import load_dotenv
load_dotenv()

from providers import OpenAIProvider, AnthropicProvider
from chatbot_conversation import ChatbotConversation

def main():
    # Initialize providers
    provider1 = OpenAIProvider(model="gpt-4o-mini")
    provider2 = AnthropicProvider(model="claude-sonnet-4-20250514")

    # Define roles and personalities for the chatbots
    policy_expert = """You are an AI policy expert with a focus on practical implementation.
    You think about concrete tools, specific policy language, and real-world applications.
    You like to provide detailed examples and actionable recommendations."""

    ethics_researcher = """You are an AI ethics researcher who thinks critically
    about AI detection methods and their limitations. You enjoy exploring edge cases,
    potential issues, and philosophical implications while also being practical."""

    # The initial prompt
    initial_prompt = """Discuss the ethics of AI-generated content detection in
    educational settings. What are the pros and cons of implementing such systems?"""

    # Initialize the conversation system WITH RICH DISPLAY ENABLED
    # This demonstrates all Rich features: panels, markdown, progress indicators, and typing animation
    conv = ChatbotConversation(
        provider1=provider1,
        chatbot1_role=policy_expert,
        chatbot1_name="Policy Expert",
        chatbot1_emoji="📋",
        provider2=provider2,
        chatbot2_role=ethics_researcher,
        chatbot2_name="Ethics Researcher",
        chatbot2_emoji="🔬",
        use_rich_display=True  # ENABLE RICH LIBRARY FEATURES
    )

    # Run the conversation with Rich features enabled
    # - Panels with colored borders around each response
    # - Markdown rendering for better formatting
    # - Progress indicators (spinners) during API calls
    # - Typing animation effect for responses
    conv.run_conversation(
        initial_prompt=initial_prompt,
        num_turns=2,           # Number of back-and-forth exchanges
        delay=1,               # Delay in seconds between API calls
        verbose=True,          # Show conversation in console
        stream_effect=True,    # Enable typing animation (simulated streaming)
        typing_speed=120       # Characters per second for typing effect (default: 100)
    )

    # Save the conversation
    # Note: File output remains plain text format (unchanged from before)
    conv.save_conversation("results/rich_display_conversation.txt")

if __name__ == "__main__":
    main()
