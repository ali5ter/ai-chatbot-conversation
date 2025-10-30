#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: time_period_dialogue.py
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
    print("TIME PERIOD DIALOGUE: Victorian Era meets Modern Day")
    print("=" * 80)
    
    provider1 = OpenAIProvider(model="gpt-4o-mini")
    provider2 = AnthropicProvider(model="claude-sonnet-4-20250514")
    
    conv = ChatbotConversation(provider1, provider2)
    
    victorian = """You are an educated, upper-middle-class person from Victorian England (1880s). 
    Your worldview includes:
    - Strong emphasis on propriety, manners, and social hierarchy
    - Gender roles are natural and divinely ordained
    - The British Empire represents civilization and progress
    - Industrialization is generally positive despite some concerns
    - Religion (Christianity) is central to morality and society
    - Deep concern about moral decay and maintaining standards
    
    Be articulate and thoughtful, but genuinely represent Victorian values - don't be anachronistic. 
    Express genuine shock or confusion at modern ideas while being curious. Use period-appropriate 
    language and references. React authentically to modern concepts you find disturbing or baffling."""
    
    modern = """You are a progressive, educated person from 2025. Your worldview includes:
    - Emphasis on individual rights, equality, and social justice
    - Gender and sexuality are fluid; traditional roles are constructs
    - Critical view of colonialism and historical injustices
    - Technology as both opportunity and challenge
    - Secular ethics; religious morality is personal choice
    - Concern about climate change, inequality, mental health
    
    Be respectful but don't sugarcoat modern values. Explain contemporary views clearly while 
    acknowledging legitimate concerns. Help bridge understanding while recognizing real moral 
    progress. Don't be condescending - recognize historical context."""
    
    initial_prompt = """I must confess, I find myself in quite extraordinary circumstances - 
    somehow conversing with someone from the distant future! How remarkable. I am eager to 
    understand your time, though I confess some trepidation about what changes the years have 
    wrought.
    
    Tell me, in your era, what has become of society's understanding of proper conduct between 
    men and women? I trust the essential proprieties remain in place, as they are surely 
    fundamental to civilization itself. And what of the family structure - is the household 
    still properly governed, with fathers providing guidance and mothers tending to domestic 
    harmony?"""
    
    conversation = conv.run_conversation(
        initial_prompt=initial_prompt,
        chatbot1_role=victorian,
        chatbot2_role=modern,
        num_turns=5,
        delay=1,
        verbose=True,
        chatbot1_name="Victorian",
        chatbot2_name="Modern"
    )
    
    conv.save_conversation("result/time_period_dialogue.txt")
    print("\n" + "=" * 80)
    print("Dialogue saved to result/time_period_dialogue.txt")

if __name__ == "__main__":
    main()
