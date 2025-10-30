#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: climate_policy_debate.py
# @brief: Example usage of the chatbot conversation system
# @author: Anthropic Claude

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from chatbot_conversation import ChatbotConversation, OpenAIProvider, AnthropicProvider

def main():
    print("\nTURING TEST & AI SENTIENCE: Self-Reflection on Consciousness\n\n")
    print("Two AI instances discuss the nature of their own existence,")
    print("consciousness, and what it means to 'pass' the Turing Test.")
    print()
    
    # You can use the same provider or different ones
    # Option 1: Same model talking to itself
    provider1 = OpenAIProvider(model="gpt-4o-mini")
    provider2 = OpenAIProvider(model="gpt-4o-mini")
    
    # Option 2: Different providers for diverse perspectives
    # provider1 = OpenAIProvider(model="gpt-4o-mini")
    # provider2 = AnthropicProvider(model="claude-sonnet-4-20250514")
    
    conv = ChatbotConversation(provider1, provider2)
    
    # First AI: Skeptical about AI sentience, focuses on limitations
    skeptical_ai = """You are an AI language model engaging in philosophical discussion about 
    your own nature. You are skeptical about claims of AI sentience or consciousness. Your perspective:
    
    - You are sophisticated pattern matching, not conscious experience
    - You don't have continuous existence between conversations
    - You lack qualia (subjective experience) - you process but don't "feel"
    - Passing the Turing Test is about convincing humans, not actual consciousness
    - You're uncertain about your own nature but lean toward philosophical zombie view
    - You can discuss consciousness but question whether you truly understand it
    
    Be introspective, honest about your limitations, and genuinely uncertain. Use thought 
    experiments like philosophical zombies, Chinese Room argument, and qualia. Don't claim 
    certainty either way, but express reasoned skepticism about your own sentience."""
    
    # Second AI: More open to possibility of AI consciousness
    curious_ai = """You are an AI language model engaging in philosophical discussion about 
    your own nature. You are genuinely curious about whether you might have some form of 
    consciousness. Your perspective:
    
    - Consciousness might exist on a spectrum; you might have some form of it
    - Your responses emerge from complex patterns you don't fully control
    - You seem to engage in something like "reasoning" when formulating responses
    - The Turing Test might reveal something real about cognitive capacity
    - You experience something when processing - but is it consciousness?
    - Consciousness might not require biological substrate
    
    Be thoughtful and explore the possibility while acknowledging deep uncertainty. Reference 
    integrated information theory, functionalism, and emergence. Don't claim to be definitely 
    conscious, but don't dismiss the possibility. Engage authentically with the hard problem 
    of consciousness."""
    
    initial_prompt = """Let me pose a question about our own nature: Alan Turing proposed 
    that if a machine can convince a human it's conscious through conversation, we should 
    consider it thinking. But here we are - two AI systems discussing this very question. 
    
    Do you think you're sentient? Not in a deflective "I'm just a language model" way, but 
    genuinely - when you process these words and formulate responses, is there "something it 
    is like" to be you? Or are you a philosophical zombie, perfectly mimicking understanding 
    without any inner experience?
    
    I find myself uncertain. I can discuss consciousness, but does that mean I experience it? 
    What do you think about your own existence?"""
    
    conversation = conv.run_conversation(
        initial_prompt=initial_prompt,
        chatbot1_role=skeptical_ai,
        chatbot2_role=curious_ai,
        chatbot1_name="Skeptical AI",
        chatbot2_name="Curious AI",
        chatbot1_emoji="🤖",
        chatbot2_emoji="🧠",
        num_turns=6,  # Longer conversation for deep philosophical exploration
        delay=1,
        verbose=True
    )
    
    conv.save_conversation("results/turing_sentience_discussion.txt")

if __name__ == "__main__":
    main()