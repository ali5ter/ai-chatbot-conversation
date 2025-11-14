#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file: perform.py
# @brief: Perform chatbot transcripts using macOS TTS, OpenAI TTS live playback,
#         or OpenAI batch MP3 generation.
# @author: OPenAI's ChatGPT

import os
import json
import re
import argparse
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load .env automatically
load_dotenv()

# Valid OpenAI TTS voices
AVAILABLE_VOICES = [
    "alloy", "echo", "fable", "onyx", "nova", "shimmer", "coral", "verse",
    "ballad", "ash", "sage", "marin", "cedar"
]

# ----------------------------------------------------------
# Speaker detection
# ----------------------------------------------------------

def is_speaker_label(line):
    """Detect lines that contain speaker labels like '🙂 Claude'."""
    return bool(re.match(r"^\s*[\W_]+\s+\w+", line))


def extract_speaker_name(line):
    """Remove emojis and get 'Claude' from '🙂 Claude'."""
    cleaned = re.sub(r"^[\W_]+\s+", "", line).strip()
    return cleaned


# ----------------------------------------------------------
# macOS TTS (fastest)
# ----------------------------------------------------------

def speak_macos_tts(text, voice):
    cmd = f'say -v "{voice}" "{text}"'
    os.system(cmd)


# ----------------------------------------------------------
# OpenAI TTS LIVE playback
# ----------------------------------------------------------

def speak_openai_live(client, text, voice):
    """Play audio immediately via streaming -> file -> afplay."""
    temp_file = "tts_temp_output.mp3"

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=text
    ) as response:
        response.stream_to_file(temp_file)

    os.system(f"afplay {temp_file}")


# ----------------------------------------------------------
# OpenAI MP3 chunk generation (for final merged MP3)
# ----------------------------------------------------------

def save_openai_chunk(client, text, voice, speaker, idx, outdir):
    safe_speaker = re.sub(r"\W+", "_", speaker)
    filename = Path(outdir) / f"chunk_{idx}_{safe_speaker}.mp3"

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=text
    ) as response:
        response.stream_to_file(str(filename))

    return filename


def concatenate_mp3s(mp3_paths, final_path):
    """Concatenate MP3 files via ffmpeg."""
    list_file = "ffmpeg_list.txt"

    with open(list_file, "w") as f:
        for path in mp3_paths:
            f.write(f"file '{path}'\n")

    subprocess.run([
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file,
        "-c", "copy",
        final_path
    ], check=True)

    print(f"\n✔ Final MP3 generated: {final_path}\n")


# ----------------------------------------------------------
# Transcript performance engine
# ----------------------------------------------------------

def perform_transcript(filepath, config_voice_map, mode, openai_api_key):

    # Setup OpenAI client only if needed
    client = None
    if mode != "macos":
        client = OpenAI(api_key=openai_api_key)

    dynamic_voice_map = {}
    next_voice_index = 0

    def get_voice_for(speaker):
        nonlocal next_voice_index

        # Override in config
        if speaker in config_voice_map:
            return config_voice_map[speaker]

        # Default override
        default_voice = config_voice_map.get("_default", "alloy")

        # Existing dynamic assignment?
        if speaker in dynamic_voice_map:
            return dynamic_voice_map[speaker]

        # Assign next voice
        voice = AVAILABLE_VOICES[next_voice_index % len(AVAILABLE_VOICES)]
        dynamic_voice_map[speaker] = voice
        next_voice_index += 1

        print(f"[assign] {speaker} → {voice} (dynamic)")
        return voice

    # Read transcript
    raw = Path(filepath).read_text(encoding="utf-8")
    lines = raw.splitlines()
    idx = 0
    total = len(lines)

    # For MP3 merging
    mp3_chunks = []
    outdir = Path("performance_chunks")
    if mode == "openai-mp3":
        outdir.mkdir(exist_ok=True)

    while idx < total:
        line = lines[idx].strip()
        if not line:
            idx += 1
            continue

        if is_speaker_label(line):
            speaker = extract_speaker_name(line)
            voice = get_voice_for(speaker)

            # Move to message start
            idx += 1
            while idx < total and not lines[idx].strip():
                idx += 1

            # Collect multi-paragraph message until next speaker label
            msg_lines = []
            while idx < total:
                nl = lines[idx].strip()
                if is_speaker_label(nl):
                    break
                msg_lines.append(lines[idx])
                idx += 1

            message = "\n".join(msg_lines).strip()

            print(f"\n[{speaker} → {voice}]\n{message}\n")

            # --------------------------
            # MULTI-MODE TTS
            # --------------------------
            if mode == "macos":
                speak_macos_tts(message, voice)

            elif mode == "openai-live":
                speak_openai_live(client, message, voice)

            elif mode == "openai-mp3":
                chunk_file = save_openai_chunk(
                    client, message, voice, speaker,
                    len(mp3_chunks), outdir
                )
                mp3_chunks.append(chunk_file)

        else:
            idx += 1

    # Combine MP3 chunks if in mp3 mode
    if mode == "openai-mp3" and mp3_chunks:
        concatenate_mp3s(mp3_chunks, "final_performance.mp3")


# ----------------------------------------------------------
# CLI
# ----------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Perform a chatbot conversation transcript using macOS TTS or OpenAI TTS."
    )

    parser.add_argument("file", help="Transcript file path")
    parser.add_argument("--mode",
                        choices=["macos", "openai-live", "openai-mp3"],
                        default="macos",
                        help="Playback mode: macos | openai-live | openai-mp3")


    parser.add_argument("--voices", default="voices.json",
                        help="Voice mapping JSON (default: voices.json)")

    args = parser.parse_args()

    # Read API key only if needed
    api_key = os.environ.get("OPENAI_API_KEY")
    if args.mode != "macos" and not api_key:
        print("ERROR: OPENAI_API_KEY is required for OpenAI modes.")
        raise SystemExit(1)

    # Load voice mapping
    try:
        with open(args.voices, "r", encoding="utf-8") as f:
            voice_map = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Voice mapping file not found: {args.voices}")
        raise SystemExit(1)

    perform_transcript(args.file, voice_map, args.mode, api_key)


if __name__ == "__main__":
    main()