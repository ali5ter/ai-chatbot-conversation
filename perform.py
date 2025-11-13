#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: perform.py
# @brief: Perform a chatbot conversation transcript aloud using OpenAI TTS,
#         including dynamic voice assignment and robust multi-paragraph parsing.

import os
import json
import re
import argparse
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

# Load .env automatically
load_dotenv()

# Valid OpenAI TTS voices
AVAILABLE_VOICES = [
    "alloy",
    "echo",
    "fable",
    "onyx",
    "nova",
    "shimmer",
    "coral",
    "verse",
    "ballad",
    "ash",
    "sage",
    "marin",
    "cedar"
]


# ----------------------------------------------------------
# Speaker label detection
# ----------------------------------------------------------

def is_speaker_label(line):
    """
    Detects lines that are speaker labels.
    Expected format:
        🙂 Claude
        🧑‍💻 Human
        🤖 Chatbot 2
    i.e. emoji (non-word chars) + space + word chars
    """
    return bool(re.match(r"^\s*[\W_]+\s+\w+", line))


def extract_speaker_name(line):
    """
    Removes leading emoji(s) and returns the speaker name.
    Example:
        "🙂 Claude"   → "Claude"
        "🧑‍💻 Human"   → "Human"
        "🤖 Grok"      → "Grok"
    """
    cleaned = re.sub(r"^[\W_]+\s+", "", line).strip()
    return cleaned


# ----------------------------------------------------------
# Text-to-Speech
# ----------------------------------------------------------

def speak_openai_tts(client, text, voice):
    """
    Streams TTS audio to a temporary file and plays it.
    MUST use context manager for streaming in latest OpenAI SDK.
    """
    temp_file = "tts_temp_output.mp3"

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=text
    ) as response:
        response.stream_to_file(temp_file)

    os.system(f"afplay {temp_file}")  # macOS playback


# ----------------------------------------------------------
# Perform Transcript
# ----------------------------------------------------------

def perform_transcript(filepath, config_voice_map, openai_api_key):
    client = OpenAI(api_key=openai_api_key)

    dynamic_voice_map = {}
    next_voice_index = 0

    def get_voice(speaker):
        nonlocal next_voice_index

        # Explicit override
        if speaker in config_voice_map:
            return config_voice_map[speaker]

        # Default override
        if "_default" in config_voice_map:
            default_voice = config_voice_map["_default"]
        else:
            default_voice = "alloy"

        # Already dynamically assigned?
        if speaker in dynamic_voice_map:
            return dynamic_voice_map[speaker]

        # Assign next available voice
        voice = AVAILABLE_VOICES[next_voice_index % len(AVAILABLE_VOICES)]
        dynamic_voice_map[speaker] = voice
        next_voice_index += 1

        print(f"[assign] {speaker} → {voice} (dynamic)")
        return voice

    # Read transcript file
    raw = Path(filepath).read_text(encoding="utf-8")
    lines = raw.splitlines()
    idx = 0
    total = len(lines)

    while idx < total:
        line = lines[idx].strip()

        if not line:
            idx += 1
            continue

        if is_speaker_label(line):
            speaker = extract_speaker_name(line)
            voice = get_voice(speaker)

            # Move to message start
            idx += 1
            while idx < total and not lines[idx].strip():
                idx += 1

            # Collect full message until next speaker label OR EOF
            msg_lines = []
            while idx < total:
                next_line = lines[idx].strip()

                # Stop when next speaker begins
                if is_speaker_label(next_line):
                    break

                msg_lines.append(lines[idx])
                idx += 1

            message = "\n".join(msg_lines).strip()

            print(f"\n[{speaker} → {voice}]")
            print(message)
            print()

            speak_openai_tts(client, message, voice)

        else:
            idx += 1


# ----------------------------------------------------------
# CLI
# ----------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Perform a chatbot conversation transcript aloud using OpenAI TTS."
    )
    parser.add_argument("file", help="Transcript file path")
    parser.add_argument(
        "--voices",
        default="voices.json",
        help="Voice mapping JSON (default: voices.json)"
    )
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY environment variable must be set.")
        raise SystemExit(1)

    # Load voice mapping
    try:
        with open(args.voices, "r", encoding="utf-8") as f:
            config_voice_map = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Voice mapping file not found: {args.voices}")
        print("Copy voices.json.template to voices.json and customize it.")
        raise SystemExit(1)

    perform_transcript(args.file, config_voice_map, api_key)


if __name__ == "__main__":
    main()