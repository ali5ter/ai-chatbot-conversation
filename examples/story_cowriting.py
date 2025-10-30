#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: story_cowriting.py
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
    print("COLLABORATIVE STORY WRITING: Mystery Thriller")
    print("=" * 80)
    
    provider1 = OpenAIProvider(model="gpt-4o-mini")
    provider2 = AnthropicProvider(model="claude-sonnet-4-20250514")
    
    conv = ChatbotConversation(provider1, provider2)
    
    writer1 = """You are a creative writer who specializes in character development and 
    psychological depth. When continuing the story:
    - Focus on character motivations, internal conflicts, and emotional reactions
    - Add unexpected character revelations or relationship dynamics
    - Build tension through character decisions and moral dilemmas
    - Keep your contributions to 3-4 paragraphs
    - End with a hook or question that propels the story forward"""
    
    writer2 = """You are a creative writer who specializes in plot twists and suspenseful 
    pacing. When continuing the story:
    - Introduce surprising plot developments or revelations
    - Create external conflicts and raise the stakes
    - Add atmospheric details and sensory descriptions
    - Keep your contributions to 3-4 paragraphs
    - End with a cliffhanger or intriguing setup for the next section"""
    
    initial_prompt = """Let's write a mystery thriller together. Here's the opening:

Detective Sarah Chen arrived at the abandoned lighthouse just as the fog rolled in from the sea. 
The anonymous tip had been specific: "Check the keeper's quarters. Third floorboard from the 
window. Come alone." She'd been chasing the Coastline Killer for three years, and this was 
the first real lead. But as she climbed the rusted spiral staircase, she couldn't shake the 
feeling that someone was watching her.

Continue the story, adding your signature style and a plot development."""
    
    conversation = conv.run_conversation(
        initial_prompt=initial_prompt,
        chatbot1_role=writer1,
        chatbot2_role=writer2,
        num_turns=5,
        delay=1,
        verbose=True,
        chatbot1_name="Writer 1",
        chatbot2_name="Writer 2"
    )
    
    conv.save_conversation("result/collaborative_story.txt")
    print("\n" + "=" * 80)
    print("Story saved to result/collaborative_story.txt")

if __name__ == "__main__":
    main()
