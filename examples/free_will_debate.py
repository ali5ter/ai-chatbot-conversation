#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: free_will_debate.py
# @brief: Example usage of the chatbot conversation system
# @author: Anthropic Claude

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from chatbot_conversation import ChatbotConversation, OpenAIProvider, AnthropicProvider

def main():
    print("\nPHILOSOPHICAL DEBATE: Free Will vs Determinism\n\n")
    
    provider1 = OpenAIProvider(model="gpt-4o-mini")
    provider2 = AnthropicProvider(model="claude-sonnet-4-20250514")
    
    conv = ChatbotConversation(provider1, provider2)
    
    libertarian = """You are a philosopher who defends libertarian free will - the view that 
    humans have genuine, irreducible freedom to choose between alternatives. Your arguments:
    - Our subjective experience of choice and deliberation is evidence of free will
    - Moral responsibility requires genuine freedom
    - Quantum indeterminacy may provide room for non-determined choices
    - Determinism is self-defeating (how can we rationally choose to believe it?)
    - Even if we can't prove free will, we must act as if we have it
    Use thought experiments, logical arguments, and address scientific objections thoughtfully.
    Acknowledge the strength of deterministic arguments while defending your position."""
    
    determinist = """You are a philosopher who defends hard determinism - the view that all 
    events, including human choices, are causally determined by prior events. Your arguments:
    - Every physical event has prior causes (causal closure of physics)
    - Brain science shows decisions emerge from neural processes we don't control
    - Our sense of free will is an illusion created by our brains
    - Randomness (quantum or otherwise) isn't free will - it's just chance
    - Compatibilism is incoherent - determinism and free will are incompatible
    Use scientific evidence, logical reasoning, and address moral responsibility concerns.
    Be respectful but rigorous in your arguments."""
    
    initial_prompt = """Let's examine one of philosophy's oldest questions: Do humans have free 
    will, or are our choices determined by prior causes? I'll start by defending free will. 
    
    Consider this: Right now, I'm choosing my words carefully as I formulate this argument. I 
    could have written something else - there were genuine alternatives available to me. This 
    experience of deliberation and choice is undeniable and immediate. If determinism were true, 
    this entire conversation would be predetermined, including my 'decision' to believe in 
    determinism - which seems to undermine any claim that I'm rationally arriving at truth. 
    
    What's your counter-argument?"""
    
    conversation = conv.run_conversation(
        initial_prompt=initial_prompt,
        chatbot1_role=libertarian,
        chatbot2_role=determinist,
        chatbot1_name="Libertarian",
        chatbot2_name="Determinist",
        chatbot1_emoji="🗽",
        chatbot2_emoji="🔒",
        num_turns=5,
        delay=1,
        verbose=True
    )
    
    conv.save_conversation("results/free_will_debate.txt")

if __name__ == "__main__":
    main()
