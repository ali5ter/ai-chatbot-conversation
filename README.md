# AI Chatbot Conversation

A Python framework for enabling conversations between two AI chatbots. Supports multiple AI providers including OpenAI, Anthropic Claude, and local models via Ollama.

## Features

- **Multiple AI Providers**: OpenAI, Anthropic Claude, Ollama (local models)
- **Mix and Match**: Have different AI models debate each other (e.g., GPT-4 vs Claude)
- **Flexible Configuration**: Customize system prompts, turn counts, and conversation parameters
- **Conversation Logging**: Save conversations to text files for later analysis
- **Extensible Design**: Easy to add new AI providers

## Installation

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/ai-chatbot-conversation.git
cd ai-chatbot-conversation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up API keys (choose based on your provider):
```bash
export OPENAI_API_KEY='your-openai-key'
export ANTHROPIC_API_KEY='your-anthropic-key'
```

## Quick Start

```python
from chatbot_conversation import ChatbotConversation, OpenAIProvider

# Create two chatbots
provider1 = OpenAIProvider(model="gpt-4o-mini")
provider2 = OpenAIProvider(model="gpt-4o-mini")

# Initialize conversation
conv = ChatbotConversation(provider1, provider2)

# Define personalities
chatbot1_system = "You are a practical AI policy expert."
chatbot2_system = "You are an AI ethics researcher."

# Start conversation
initial_prompt = "Let's discuss AI safety in education."

conversation = conv.run_conversation(
    initial_prompt=initial_prompt,
    chatbot1_system=chatbot1_system,
    chatbot2_system=chatbot2_system,
    num_turns=3
)

# Save results
conv.save_conversation("my_conversation.txt")
```

## Supported Providers

### OpenAI
```python
from chatbot_conversation import OpenAIProvider
provider = OpenAIProvider(model="gpt-4o-mini")
```

### Anthropic Claude
```python
from chatbot_conversation import AnthropicProvider
provider = AnthropicProvider(model="claude-sonnet-4-20250514")
```

### Ollama (Local Models)
```python
from chatbot_conversation import OllamaProvider
provider = OllamaProvider(model="llama2")
```

## Examples

See the `examples/` directory for more use cases:
- `basic_conversation.py` - Simple two-chatbot conversation
- More examples coming soon!

## Configuration

Customize conversations with these parameters:

- `initial_prompt`: Starting message for the conversation
- `chatbot1_system` / `chatbot2_system`: System prompts defining chatbot personalities
- `num_turns`: Number of back-and-forth exchanges
- `delay`: Seconds between API calls (to avoid rate limits)
- `verbose`: Whether to print conversation to console

## Use Cases

- **Research**: Study how different AI models approach the same problem
- **Brainstorming**: Generate diverse ideas by having AIs with different personas discuss topics
- **Testing**: Compare responses across different AI providers
- **Education**: Demonstrate AI capabilities and limitations
- **Content Generation**: Create dialogue for stories, scripts, or educational materials

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Acknowledgments

Built with support from:
- OpenAI API
- Anthropic Claude API
- Ollama for local model support
