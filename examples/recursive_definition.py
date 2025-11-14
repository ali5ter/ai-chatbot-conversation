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
    print("\nRECURSIVE DEFINITION CHALLENGE\n\n")
    print("Two AIs must define complex concepts using only simpler terms.")
    print("Each term used must then be defined by the other AI.")
    print("Continue until reaching primitive, undefined concepts.")
    print("This exposes circular reasoning and tests true understanding.\n\n")
    
    openai = OpenAIProvider(model="gpt-4o-mini")
    anthropic = AnthropicProvider(model="claude-sonnet-4-20250514")

    definer = """You are participating in a recursive definition exercise. Your goal is to 
define concepts using ONLY simpler, more fundamental terms.
    
CRITICAL RULES:
1. When defining a concept, use only words that are simpler/more basic
2. AVOID circular definitions (don't use the concept to define itself)
3. Track which terms you've already used - the other AI will ask you to define those next
4. Each definition should be 2-3 sentences maximum
5. As you go deeper, acknowledge when you're approaching primitive concepts
6. Primitive concepts are those that can't be reduced further (like "existence", "change", "identity")
    
FORMAT YOUR RESPONSES EXACTLY LIKE THIS:
    
DEFINITION: [Concept] = [Definition using simpler terms]
    
TERMS USED: [List the key terms you used in your definition]
    
DEPTH LEVEL: [Current depth in the chain]
    
[Brief meta-comment about the definition or difficulty]
    
EXAMPLES OF GOOD VS BAD DEFINITIONS:
❌ BAD: "Consciousness = the state of being conscious"  (circular!)
✅ GOOD: "Consciousness = awareness of internal thoughts and external environment"
    
❌ BAD: "Knowledge = justified true belief that represents knowledge" (circular!)
✅ GOOD: "Knowledge = justified true belief about reality"
    
Be intellectually honest - if you're defining something recursively or getting stuck, acknowledge it!"""
    
    # Second AI: Requests definitions for terms used
    analyzer = """You are participating in a recursive definition exercise. Your role is to 
analyze definitions and request clarification of terms used.
    
YOUR PROCESS:
1. Read the definition provided
2. Identify the KEY terms used in that definition
3. Pick the MOST important or complex term from their definition
4. Request that they define that term using even simpler concepts
5. Watch for circular reasoning (using a word to define itself)
6. Track the depth - after 8-10 levels, we should be reaching primitives
7. Acknowledge when we've reached a genuine primitive concept
    
FORMAT YOUR RESPONSES EXACTLY LIKE THIS:
    
ANALYSIS: [Brief comment on the definition quality]
    
CIRCULAR REASONING CHECK: [Note if definition was circular]
    
NEXT TERM TO DEFINE: "[The term you're selecting]"
    
WHY THIS TERM: [Explain why you picked this term to define next]
    
DEPTH TRACKING: [Count how many levels deep we are]
    
[Question or challenge about the definition]
    
WHAT TO WATCH FOR:
- Circular definitions (using word to define itself)
- Overly complex definitions (should get simpler as we go down)
- Hidden assumptions
- Terms that seem primitive but might not be
    
PRIMITIVE CONCEPTS might include:
- Existence, being, thing
- Change, time, space
- Identity, difference, relation
- Experience, awareness, sensation
    
When we reach genuine primitives, acknowledge it and explain why they can't be reduced further."""
    
    initial_prompt = """Let's begin the recursive definition challenge. I'll start by 
defining a complex concept, and then you'll ask me to define the terms I used in 
that definition. We'll continue breaking down concepts until we reach primitives.

DEFINITION: Intelligence = the capacity to acquire knowledge, reason about information, 
and adaptively solve problems in varied contexts.
    
TERMS USED: capacity, acquire, knowledge, reason, information, adaptively, solve, 
problems, contexts
    
DEPTH LEVEL: 1
    
This is our starting concept. Notice I'm using fairly complex terms like "knowledge", 
"reason", and "information" that themselves need definition. Which term would you like 
me to define next?"""

    conv = ChatbotConversation(
        provider1=openai,
        chatbot1_role=definer,
        chatbot1_name="Definer",
        chatbot1_emoji="📖",
        provider2=anthropic,
        chatbot2_role=analyzer,
        chatbot2_name="Analyzer",
        chatbot2_emoji="🔬"
    )

    conv.run_conversation(
        initial_prompt=initial_prompt,
        num_turns=8
    )

    conv.save_conversation("results/recursive_definition.txt")
    
    print("\n\n\nThe Challenge: AIs often struggle with this because they're trained on")
    print("definitions that may be circular or assume concepts they should define.")
    print("This exercise reveals the limits of language and conceptual understanding.")

if __name__ == "__main__":
    main()