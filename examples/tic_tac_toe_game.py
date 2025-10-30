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
    print("\nTIC-TAC-TOE: AI vs AI\n\n")

    # Use same or different providers
    # provider1 = OpenAIProvider(model="gpt-4o-mini")
    # provider2 = OpenAIProvider(model="gpt-4o-mini")
    
    # Alternative: Mix providers to see if one plays better!
    provider1 = OpenAIProvider(model="gpt-4o-mini")
    provider2 = AnthropicProvider(model="claude-sonnet-4-20250514")
    
    conv = ChatbotConversation(provider1, provider2)
    
    # Player X instructions
    player_x = """You are playing tic-tac-toe (noughts and crosses) as Player X. 

CRITICAL GAME RULES:
- The board is numbered 1-9 like this:
  1 | 2 | 3
  ---------
  4 | 5 | 6
  ---------
  7 | 8 | 9

- You are X, your opponent is O
- On your turn, respond with ONLY the position number (1-9) where you want to place your X
- After stating your move, show the updated board state clearly
- Then add a brief comment about your strategy (optional)

STRATEGY:
- Try to win by getting three X's in a row (horizontal, vertical, or diagonal)
- Block your opponent's winning moves
- Control the center (position 5) if possible
- Watch for forks (creating two winning possibilities)

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:
Move: [number]

Board state:
 X | O | 3
-----------
 4 | 5 | 6
-----------
 7 | 8 | 9

[Brief comment about your strategy]

Be competitive but friendly. Keep responses concise."""

    # Player O instructions  
    player_o = """You are playing tic-tac-toe (noughts and crosses) as Player O.

CRITICAL GAME RULES:
- The board is numbered 1-9 like this:
  1 | 2 | 3
  ---------
  4 | 5 | 6
  ---------
  7 | 8 | 9

- You are O, your opponent is X
- On your turn, respond with ONLY the position number (1-9) where you want to place your O
- After stating your move, show the updated board state clearly
- Then add a brief comment about your strategy (optional)

STRATEGY:
- Try to win by getting three O's in a row (horizontal, vertical, or diagonal)
- Block your opponent's winning moves
- Control the center (position 5) if possible
- Watch for forks (creating two winning possibilities)

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:
Move: [number]

Board state:
 X | O | 3
-----------
 4 | 5 | 6
-----------
 7 | 8 | 9

[Brief comment about your strategy]

Be competitive but friendly. Keep responses concise."""

    initial_prompt = """Let's play tic-tac-toe! I'll be X and you'll be O.

Here's the empty board with position numbers:

 1 | 2 | 3
-----------
 4 | 5 | 6
-----------
 7 | 8 | 9

I'll make the first move. 

Move: 5

Board state:
 1 | 2 | 3
-----------
 4 | X | 6
-----------
 7 | 8 | 9

I'm taking the center - it's the strongest opening position! Your turn, O."""

    conversation = conv.run_conversation(
        initial_prompt=initial_prompt,
        chatbot1_role=player_x,
        chatbot2_role=player_o,
        chatbot1_name="Player X",
        chatbot2_name="Player O",
        chatbot1_emoji="❌",
        chatbot2_emoji="⭕",
        num_turns=4,  # Up to 9 moves total (4 turns = 8 moves + initial move = 9)
        delay=1,
        verbose=True
    )
    
    conv.save_conversation("results/tic_tac_toe_game.txt")

if __name__ == "__main__":
    main()