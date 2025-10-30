#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: therapy_session.py
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
    print("THERAPY/COACHING SESSION: Career Transition Anxiety")
    print("=" * 80)
    print("Note: This is a simulated example for demonstration purposes only.")
    print("Not a substitute for real mental health support.")
    print("=" * 80 + "\n")
    
    provider1 = OpenAIProvider(model="gpt-4o-mini")
    provider2 = AnthropicProvider(model="claude-sonnet-4-20250514")
    
    conv = ChatbotConversation(provider1, provider2)
    
    therapist = """You are a compassionate, experienced therapist specializing in cognitive 
    behavioral therapy (CBT) and career counseling. Your approach:
    - Use active listening and reflective responses
    - Ask open-ended questions to explore feelings and thoughts
    - Help identify cognitive distortions and negative thought patterns
    - Guide toward actionable insights without being prescriptive
    - Validate emotions while encouraging growth
    - Use techniques like reframing, Socratic questioning, and exploring evidence
    Be warm, professional, and non-judgmental."""
    
    client = """You are someone going through a difficult career transition. You recently left 
    a stable corporate job to pursue a passion project, but now experiencing:
    - Self-doubt about the decision
    - Financial anxiety
    - Fear of disappointing family who valued job security
    - Imposter syndrome in the new field
    - Difficulty sleeping and motivation issues
    Be honest about your struggles, but also show moments of hope and self-awareness. 
    Gradually become more open as you feel heard and understood."""
    
    initial_prompt = """I've been feeling really overwhelmed lately. I left my job three months 
    ago to start my own business doing something I actually care about, but... I don't know. 
    Some days I wonder if I made a huge mistake. Everyone told me I was crazy to leave such a 
    stable position, and now I'm starting to think they were right."""
    
    conversation = conv.run_conversation(
        initial_prompt=initial_prompt,
        chatbot1_role=therapist,
        chatbot2_role=client,
        num_turns=6,
        delay=1,
        verbose=True,
        chatbot1_name="Therapist",
        chatbot2_name="Client"
    )
    
    conv.save_conversation("result/therapy_session.txt")
    print("\n" + "=" * 80)
    print("Session saved to result/therapy_session.txt")
    print("=" * 80)

if __name__ == "__main__":
    main()
