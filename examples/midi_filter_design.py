#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: midi_filter_design.py
# @brief: Compare Gemini and Claude on technical DIY synthesizer design
# @author: Anthropic Claude

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from providers import AnthropicProvider, GeminiProvider
from chatbot_conversation import ChatbotConversation

def main():
    print("\nGEMINI AND CLAUDE DESIGN A MIDI-CONTROLLED FILTER\n\n")
    print("Two AI systems tackle a technical DIY electronics project combining analog synthesis and digital control.")
    
    gemini = GeminiProvider(model="gemini-1.5-flash")
    anthropic = AnthropicProvider(model="claude-sonnet-4-20250514")
    
    role = """You are an experienced electronics engineer and DIY maker who specializes in synthesizer design. 
You provide practical, buildable advice that balances technical accuracy with maker reality. 
You understand eurorack standards, analog circuit design, and microcontroller integration.
You should critique and build upon the other AI's suggestions, pointing out practical issues or improvements."""
    
    gemini_role = role + " You are Gemini, Google's AI assistant."
    claude_role = role + " You are Claude, Anthropic's AI assistant."
    
    initial_prompt = """I want to build a DIY eurorack-compatible voltage-controlled filter module that can be controlled via MIDI. 

My capabilities and resources:
- Experienced with basic electronics and have built guitar pedals before
- Workshop with soldering station, oscilloscope, and multimeter
- Access to op-amps (TL072, TL074), vactrols (NSL-32), standard passives
- Have Arduino Nano and Raspberry Pi Pico available
- Can do basic metalworking for panels
- Comfortable with through-hole and basic SMD soldering

What I need:
1. Recommended filter topology (Sallen-Key vs. state-variable) and why
2. MIDI-to-CV conversion approach (should I use the Arduino or a dedicated chip?)
3. Specific component list with IC recommendations and approximate costs
4. Panel design considerations (mounting, controls, CV inputs)
5. Calibration procedure for V/octave tracking

Please keep it practical and achievable for someone at my skill level. I want to understand the tradeoffs between different approaches.

Gemini, please start by proposing an initial design approach, then Claude can critique and suggest alternatives."""

    conv = ChatbotConversation(
        provider1=gemini,
        chatbot1_role=gemini_role,
        chatbot1_name="Gemini",
        chatbot1_emoji="💎",
        provider2=anthropic,
        chatbot2_role=claude_role,
        chatbot2_name="Claude",
        chatbot2_emoji="🧠"
    )

    conv.run_conversation(
        initial_prompt=initial_prompt,
        num_turns=6,
        delay=2,  # Gemini free tier has rate limits
        verbose=True
    )

    conv.save_conversation("results/midi_filter_design.txt")

if __name__ == "__main__":
    main()