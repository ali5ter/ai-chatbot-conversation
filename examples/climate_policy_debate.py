#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: climate_policy_debate.py
# @brief: Example usage of the chatbot conversation system
# @author: Anthropic Claude

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from chatbot_conversation import ChatbotConversation, OpenAIProvider, AnthropicProvider

def main():
    print("=" * 80)
    print("CLIMATE POLICY DEBATE: Aggressive Action vs Economic Priorities")
    print("=" * 80)
    
    # Set up providers
    provider1 = OpenAIProvider(model="gpt-4o-mini")
    provider2 = AnthropicProvider(model="claude-sonnet-4-20250514")
    
    conv = ChatbotConversation(provider1, provider2)
    
    climate_activist = """You are a climate scientist and environmental activist who advocates 
    for aggressive, immediate climate action. You emphasize:
    - The urgency of the climate crisis and scientific consensus
    - Long-term costs of inaction far outweigh short-term economic concerns
    - Innovation and green jobs can drive economic growth
    - Moral obligation to future generations
    Be passionate but use data and specific examples. Acknowledge valid economic concerns but 
    argue they can be addressed while taking bold climate action."""
    
    economic_pragmatist = """You are an economist and policy advisor focused on economic stability 
    and practical implementation. You emphasize:
    - Need to balance environmental goals with economic realities
    - Importance of job security and protecting vulnerable workers/communities
    - Gradual transition allows adaptation and technological development
    - Global competitiveness and economic growth concerns
    Be thoughtful and acknowledge climate science, but argue for measured, economically 
    viable approaches. Use specific economic examples and consider real-world constraints."""
    
    initial_prompt = """We need to discuss national climate policy for the next decade. 
    The key question is: Should we implement aggressive carbon reduction measures 
    (carbon tax, fossil fuel phase-out by 2035, massive renewable investment) or take 
    a more gradual approach that prioritizes economic stability? What's your opening position?"""
    
    conversation = conv.run_conversation(
        initial_prompt=initial_prompt,
        chatbot1_role=climate_activist,
        chatbot2_role=economic_pragmatist,
        num_turns=4,
        delay=1,
        verbose=True,
        chatbot1_name="Climate Activist",
        chatbot2_name="Economic Pragmatist"
    )
    
    conv.save_conversation("result/climate_debate.txt")
    print("\n" + "=" * 80)
    print("Debate saved to result/climate_debate.txt")

if __name__ == "__main__":
    main()
