# Room Cleaning Agent

An intelligent agent based on LangChain and Google Gemini that autonomously cleans rooms using logical reasoning to execute sequential actions.

## Description

This project implements an AI agent that simulates room cleaning. The agent analyzes the current state of the environment and executes specific actions to achieve the desired organizational state, following the ReAct (Reasoning + Acting) pattern.

### Room State

The room has three main elements:

- **Clothes**: Can be on the `floor`, in your `hand` or in the `hamper`
- **Books**: Can be `scattered`, in your `hand` or on the `shelf`
- **Wastebin**: Can be `full` or `empty`

### Goal

Transform the initial state:
```python
{
    "clothes": "floor",
    "books": "scattered",
    "wastebin": "full"
}
```

Into the desired state:
```python
{
    "clothes": "hamper",
    "books": "shelf",
    "wastebin": "empty"
}
```

## Available Tools

The agent has access to the following tools:

1. **check_final_step**: Checks if the current state matches the desired final state
2. **pick_up_clothes**: Picks up clothes from the floor and holds them in hand
3. **put_clothes_in_hamper**: Puts clothes from hand into the hamper
4. **pick_up_books**: Picks up books and holds them in hand
5. **place_books_on_shelf**: Places books from hand onto the shelf
6. **empty_wastebin**: Empties the wastebin when it's full

## Installation

### Prerequisites

- Python 3.8 or higher
- Google Gemini API Key

### Steps

1. Clone the repository:
```bash
git clone <repository-url>
cd example_room
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure your Google Gemini API key:
```bash
export GOOGLE_API_KEY="your-api-key-here"
```

## Usage

Run the agent:
```bash
python main.py
```

The agent will:
1. Analyze the initial state of the room
2. Reason about the necessary actions
3. Execute the appropriate tools in sequence
4. Verify if it has reached the desired final state

## Execution Example

```
Thought: The clothes are on the floor. I should pick them up.
Action: pick_up_clothes
Action Input: {"clothes": "floor", "books": "scattered", "wastebin": "full"}
Observation: The room is not yet tidy. Continue working

Thought: Now I have the clothes in my hand. I should put them in the hamper.
Action: put_clothes_in_hamper
Action Input: {"clothes": "hand", "books": "scattered", "wastebin": "full"}
Observation: The room is not yet tidy. Continue working

...

Final Answer: The room is tidy. Final state achieved.
```

## Architecture

The project uses:

- **LangChain**: Framework for developing applications with LLMs
- **Google Gemini (gemini-2.5-pro)**: Language model for reasoning and decision making
- **ReAct Pattern**: Pattern that combines Reasoning with Acting

### Main Components

1. **Tools**: Functions decorated with `@tool` that represent actions the agent can execute
2. **Agent**: Implemented using `create_react_agent` from LangChain
3. **AgentExecutor**: Executes the agent with a maximum limit of 10 steps

## Dependencies

- `langchain-community==0.3.7`
- `langchain-core==0.3.20`
- `langchain-google-genai==2.0.5`

## Configuration

### Modifying the Initial State

You can modify the room's initial state by editing the `room_state` variable in `main.py`:

```python
room_state = {
    "clothes": "floor",      # or "hand", "hamper"
    "books": "scattered",    # or "hand", "shelf"
    "wastebin": "full"       # or "empty"
}
```

### Modifying the Desired State

Edit the `DESIRED_STATE` constant to define new goals:

```python
DESIRED_STATE = {
    "clothes": "hamper",
    "books": "shelf",
    "wastebin": "empty"
}
```

## Technical Features

- **State Validation**: Robust validation system that accepts Python dictionaries or JSON strings
- **Error Handling**: Configured with `handle_parsing_errors=True` for greater resilience
- **Verbose Mode**: Detailed output of the agent's reasoning process
- **Step Limit**: Maximum of 10 iterations to prevent infinite loops

## Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest new features
- Add new tools to the agent
- Improve documentation

## License

This project is provided as an educational example.

## Author

Fernando Ferreira

**Note**: This is a demonstration project that illustrates the use of AI agents for problem solving through sequential reasoning and action.
