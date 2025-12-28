# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python framework for orchestrating conversations between two AI chatbots. It supports multiple AI providers (OpenAI, Anthropic, xAI Grok, Google Gemini, Ollama) and allows different models to debate, collaborate, or discuss topics with each other.

## Core Architecture

### Provider Pattern

All AI providers inherit from the `ChatProvider` abstract base class in `providers.py`:
- Each provider implements `get_response(system_prompt, messages, temperature, max_tokens)`
- Providers handle their own API authentication, message formatting, and response extraction
- Environment variables control both API keys and default settings (temperature, max_tokens)
- Each provider can use global defaults (`DEFAULT_TEMPERATURE`, `DEFAULT_MAX_TOKENS`) or provider-specific overrides (`OPENAI_TEMPERATURE`, `ANTHROPIC_MAX_TOKENS`, etc.)

### Conversation Management

`ChatbotConversation` class (`chatbot_conversation.py`) orchestrates the dialogue:
- Takes two providers (can be same or different types)
- Maintains conversation history in OpenAI message format (`role`, `content`)
- Alternates turns between chatbots by reversing message roles for the second chatbot
- Initial prompt is treated as coming from chatbot1 (`assistant` role)
- **Key insight**: Each chatbot sees the conversation from their perspective - chatbot2's messages are reversed so `assistant` becomes `user` and vice versa

### Message Flow

```
Initial Prompt (assistant)
→ Chatbot 2 responds (sees prompt as user message)
→ Chatbot 1 responds (sees Chatbot 2 as user message)
→ Repeat for num_turns
```

## Development Commands

### Installation
```bash
pip install -r requirements.txt
```

### Running Examples
```bash
# Run any example from the root directory
python examples/basic_conversation.py
python examples/climate_policy_debate.py
python examples/story_cowriting.py

# Examples automatically add parent directory to sys.path to import providers
```

### Environment Setup
API keys are loaded from environment variables or `.env` file via `python-dotenv`:
```bash
# Required for different providers
export OPENAI_API_KEY='your-key'
export ANTHROPIC_API_KEY='your-key'
export XAI_API_KEY='your-key'
export GEMINI_API_KEY='your-key'

# Optional: control default behavior
export DEFAULT_TEMPERATURE=0.7
export DEFAULT_MAX_TOKENS=500
export OPENAI_TEMPERATURE=0.8    # Provider-specific override
```

### TTS Performance (perform.py)
Three modes for performing saved conversations with text-to-speech:

```bash
# macOS built-in TTS (fastest, no API needed)
python perform.py conversation.txt --mode macos

# OpenAI live streaming (plays as it generates)
python perform.py conversation.txt --mode openai-live

# Generate single MP3 file (requires ffmpeg)
python perform.py conversation.txt --mode openai-mp3
```

Voice mapping in `voices.json` controls which voice speaks for each chatbot name.

## File Structure

- `providers.py` - All AI provider implementations
- `chatbot_conversation.py` - Core conversation orchestration
- `perform.py` - TTS playback of saved conversations
- `examples/` - Demonstration scripts showing different conversation types
- `my_prompts/` - Custom user prompts (not part of core framework)

## Key Implementation Details

### Provider-Specific Quirks

**Google Gemini** (`GoogleProvider`):
- Uses `system_instruction` parameter instead of system message in conversation
- Has safety filters that may block responses - code handles blocked responses gracefully
- Finish reasons: STOP (1), SAFETY (2), RECITATION (3), MAX_TOKENS (4), OTHER (5)
- Message history formatted differently (uses `model` role instead of `assistant`)

**Anthropic Claude** (`AnthropicProvider`):
- System prompt passed separately via `system` parameter
- Messages use same role names as OpenAI

**xAI Grok** (`xAIGrokProvider`):
- Uses OpenAI SDK with custom `base_url="https://api.x.ai/v1"`
- Otherwise behaves identically to OpenAI

**Ollama** (`OllamaProvider`):
- Local models, no API key needed
- Builds prompt string manually instead of structured messages
- Uses `requests` library directly instead of SDK

### Error Handling

- Providers catch API errors and return formatted error strings
- Google Gemini provider has extensive error handling for safety filters
- Blocked content returns descriptive messages rather than crashing

### Conversation Saving

- `save_conversation()` writes to text files with emoji + name headers
- Format matches what `perform.py` expects for TTS playback
- Creates parent directories automatically if they don't exist

## Adding New Providers

1. Inherit from `ChatProvider` in `providers.py`
2. Implement `__init__` with API key validation and model setup
3. Implement `get_response()` to handle message format conversion and API calls
4. Add provider-specific environment variable support (`PROVIDER_TEMPERATURE`, etc.)
5. Print initialization confirmation showing model and defaults
