#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: midi_vcf_design.py
# @brief: Avoid "filter" keyword which seems to trigger Gemini safety

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from providers import AnthropicProvider, GoogleProvider
from chatbot_conversation import ChatbotConversation

def main():
    print("\nGEMINI AND CLAUDE DESIGN A MIDI-CONTROLLED VCF\n\n")
    print("Two AI systems discuss voltage-controlled audio circuitry.")
    
    # Try gemini-2.0-flash instead of 2.5
    google = GoogleProvider(model="gemini-2.0-flash", temperature=0.5)
    anthropic = AnthropicProvider(model="claude-sonnet-4-20250514")
    
    role = """You are an experienced audio electronics engineer specializing in synthesizer circuits. 
You provide practical, buildable advice for DIY projects. 
You share your knowledge and build on others' suggestions."""
    
    gemini = role + " You are Gemini."
    claude = role + " You are Claude."
    
    # Reword to avoid "filter" - use VCF (Voltage Controlled Filter) acronym and "circuit"
    initial_prompt = """I want to build a DIY eurorack-compatible VCF (voltage-controlled frequency circuit) that responds to MIDI control.

My background:
- Built guitar pedals before
- Have workshop with soldering station, oscilloscope, multimeter
- Access to op-amps: TL072, TL074, vactrols NSL-32, standard passives
- Have Arduino Nano and Raspberry Pi Pico
- Can do basic metalworking for front panels
- Comfortable with through-hole and basic SMD soldering

Questions:
1. Recommended VCF topology: Sallen-Key or state-variable? Why?
2. MIDI-to-CV conversion: Arduino, Pico, or dedicated chip?
3. Component list with specific ICs and approximate costs
4. Front panel design: mounting, controls, CV inputs
5. Calibration procedure for V/octave tracking

Please provide practical advice for someone at my skill level. I want to understand the tradeoffs.

Gemini, please start with your recommendations for the VCF topology."""

    conv = ChatbotConversation(
        provider1=anthropic,
        chatbot1_role=claude,
        chatbot1_name="Claude",
        chatbot1_emoji="🧠",
        provider2=google,
        chatbot2_role=gemini,
        chatbot2_name="Gemini",
        chatbot2_emoji="💎"
    )

    conv.run_conversation(
        initial_prompt=initial_prompt,
        num_turns=6,
        delay=3,
        verbose=True
    )

    conv.save_conversation("results/midi_vcf_design.txt")
    print("\n✅ Conversation saved!")

if __name__ == "__main__":
    main()