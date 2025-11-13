# 🤖 AI Chatbot Conversation

A Python framework for enabling conversations between two AI chatbots. Supports multiple AI providers including OpenAI, Anthropic Claude, and local models via Ollama.

## Features

- **Multiple AI Providers**: OpenAI ChatGPT, Anthropic Claude, xAI Grok, and Ollama (local models)
- **Mix and Match**: Have different AI models debate each other (e.g., GPT-4 vs Claude)
- **Flexible Configuration**: Customize system prompts, turn counts, and conversation parameters
- **Conversation Logging**: Save conversations to text files for later analysis
- **Extensible Design**: Easy to add new AI providers

## Installation

1.Clone this repository:

```bash
git clone https://github.com/YOUR_USERNAME/ai-chatbot-conversation.git
cd ai-chatbot-conversation
```

2.Install dependencies:

```bash
pip install -r requirements.txt
```

3.Get your API keys (see [Getting API Keys](#getting-api-keys) section below)

4.Set up API keys as environment variables:

```bash
export OPENAI_API_KEY='your-openai-key'
export ANTHROPIC_API_KEY='your-anthropic-key'
```

Or create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
```

## Getting API Keys

### OpenAI API Key

1. **Create an OpenAI Account**
   - Go to the [OpenAI website](https://platform.openai.com/signup)
   - Sign up with your email or Google/Microsoft account

2. **Add Payment Method**
   - Navigate to the [billing page](https://platform.openai.com/account/billing/overview)
   - Click "Add payment method"
   - Add a credit/debit card (OpenAI uses pay-as-you-go pricing)
   - Consider [setting up usage limits](https://platform.openai.com/account/limits)

3. **Generate API Key**
   - Go to the [API keys page](https://platform.openai.com/api-keys)
   - Click "Create new secret key"
   - Give it a name (e.g., "chatbot-conversation")
   - **Important**: Copy the key immediately - you won't be able to see it again!
   - Store it securely (never commit it to Git)

4. **Pricing** (as of 2025)
   - GPT-4o-mini: ~$0.15 per 1M input tokens, ~$0.60 per 1M output tokens
   - GPT-4o: ~$2.50 per 1M input tokens, ~$10 per 1M output tokens
   - Check [current pricing](https://openai.com/api/pricing/)

### Anthropic Claude API Key

1. **Create an Anthropic Account**
   - Go to the [Athropic website](https://console.anthropic.com/)
   - Click "Sign Up" and create an account with your email

2. **Add Credits**
   - Navigate to the [billing page](https://console.anthropic.com/settings/billing)
   - Click "Add credits" or "Add payment method"
   - Purchase credits (minimum $5) or set up auto-recharge
   - Anthropic uses a prepaid credit system

3. **Generate API Key**
   - Go to the [API keys page](https://console.anthropic.com/settings/keys)
   - Click "Create Key"
   - Give it a name (e.g., "chatbot-conversation")
   - **Important**: Copy the key immediately - it won't be shown again!
   - Store it securely

4. **Pricing** (as of 2025)
   - Claude Sonnet 4: ~$3 per 1M input tokens, ~$15 per 1M output tokens
   - Claude Opus 4: ~$15 per 1M input tokens, ~$75 per 1M output tokens
   - Check the [current pricing](https://www.anthropic.com/pricing)

### xAI API key

1. **Create an xAI account**
   - Navigate to the [the xAI accounts site](https://accounts.x.ai/)
   - Click Log in and then sign up.

2. **Add credits**
   - Navigate to the [xAI console](https://console.x.ai)
   - Click "Purchace" to purchace credits
   - Purchase credits (minimum $5)

3. **Generate API Key**
   - Click "Create" to create your first API key
   - **Important**: Copy the key immediately - it won't be shown again!
   - Store it securely

### Security Best Practices

⚠️ **Never commit API keys to Git!**

- Use environment variables or a `.env` file (which is in `.gitignore`)
- Rotate keys periodically
- Set up usage limits/budgets on both platforms
- Use separate keys for development and production
- Consider using tools like `python-dotenv` for managing environment variables:

```bash
pip install python-dotenv
```

Then in your Python script:

```python
from dotenv import load_dotenv
load_dotenv()  # This loads variables from .env file
```

## Quick Start

```python
from chatbot_conversation import ChatbotConversation, OpenAIProvider

# Create two chatbots
provider1 = OpenAIProvider(model="gpt-4o-mini")
provider2 = OpenAIProvider(model="gpt-4o-mini")

# Initialize conversation
conv = ChatbotConversation(provider1, provider2)

# Define roles
chatbot1_role = "You are a practical AI policy expert."
chatbot2_role = "You are an AI ethics researcher."

# Start conversation
initial_prompt = "Let's discuss AI safety in education."

conversation = conv.run_conversation(
    initial_prompt=initial_prompt,
    chatbot1_role=chatbot1_system,
    chatbot2_role=chatbot2_system,
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

### xAI Grok

```python
from chatbot_conversation import xAIGrokProvider
provider = xAIGrokProvider(model="grok-4")
```

### Ollama (Local Models)

```python
from chatbot_conversation import OllamaProvider
provider = OllamaProvider(model="llama2")
```

## Examples

See the `examples/` directory for more use cases:

### Basic Usage

- **`basic_conversation.py`** - Simple AI policy discussion (original example)

### Debates & Arguments

- **`climate_policy_debate.py`** - Climate scientist vs economist debating aggressive climate action vs economic priorities
- **`free_will_debate.py`** - Libertarian free will vs hard determinism philosophical debate

### Creative & Collaborative

- **`story_cowriting.py`** - Two writers collaboratively building a mystery thriller with alternating plot twists and character development

### Educational & Exploratory

- **`time_period_dialogue.py`** - Victorian-era person encountering modern social norms and values
- **`therapy_session.py`** - Simulated therapy session exploring career transition anxiety (educational demonstration only)

Other examples may be added.

Run any example:

```bash
python examples/climate_policy_debate.py
python examples/story_cowriting.py
```

Each example demonstrates different conversation styles and can be customized for your needs.

## Configuration

Customize conversations with these parameters:

- `initial_prompt`: Starting message for the conversation
- `chatbot1_role` / `chatbot2_role`: Role descriptions defining chatbot personalities
- `chatbot1_name` / `chatbot2_name`: Short name for each chatbot
- `chatbot1_emoji` / `chatbot2_emoji`: An icon for each chatbot
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
