DESIRED_STATE = {
    "clothes": "hamper",
    "books": "shelf",
    "wastebin": "empty"
}

room_state = {
    "clothes": "floor",
    "books": "scattered",
    "wastebin": "full"
}

# 1. Clothes : floor -> hand -> hamper
# 2. Books: scattered -> hand -> shelf
# 3. Wastebin: Full -> Empty

from langchain.tools import tool
import json


def is_clean(state):
    """
    Check whether room is already cleaned
    
    :param state: Current room state
    :return: Flag showing whether the room is cleaned
    :rtype: bool
    """
    return all(state[item] == DESIRED_STATE[item] for item in DESIRED_STATE)

def validate_and_convert_state(state: dict|str) -> dict:
    """
    Check whether state dictionary is actually a dictionary and
    convert it otherwise
    
    :param state: room state (as json string or dictionary)
    :return: room state as a dictionary
    :rtype: dictionary 
    """
    if isinstance(state, str):
        try:
            state = state.replace("'", "\"")
            state = json.loads(state)
        except json.JSONDecodeError:
            raise ValueError("Invalid state format. Please provide a valid dict or"
                             " JSON string")
    if not isinstance(state, dict):
        raise ValueError("Invalid state format")
    return state

# TOOLS
@tool
def check_final_step(state: dict|str) -> str:
    """
    Check whether the current state matches the final state
    """
    state = validate_and_convert_state(state)
    if is_clean(state):
        return "The room is tidy. Final state achieved."
    return "The room is not yet tidy. Continue working."

@tool
def pick_up_clothes(state: dict|str) -> str:
    """
    Picks up clothes from the floor and holds in the hand
    """
    state = validate_and_convert_state(state)
    state['clothes'] = "hand"
    return json.dumps(state)

@tool
def put_clothes_in_hamper(state: dict|str) -> str:
    """
    Puts clothes from hand into the hamper
    """
    state = validate_and_convert_state(state)
    state['clothes'] = "hamper"
    return json.dumps(state)

@tool
def pick_up_books(state: dict|str) -> str:
    """
    Picks up books from the floor and holds in the hand
    """
    state = validate_and_convert_state(state)
    state['books'] = "hand"
    return json.dumps(state)


@tool
def place_books_on_shelf(state: dict|str) -> str:
    """
    Place books from hand to the shelf
    """
    state = validate_and_convert_state(state)
    state['books'] = "shelf"
    return json.dumps(state)


@tool
def empty_wastebin(state: dict|str) -> str:
    """
    Empties the wastebin if it is full.
    """
    state = validate_and_convert_state(state)
    state['wastebin'] = "empty"
    return json.dumps(state)

tools = [
    check_final_step,
    pick_up_clothes,
    put_clothes_in_hamper,
    pick_up_books,
    place_books_on_shelf,
    empty_wastebin
]


# AGENT

from langchain_google_genai import GoogleGenerativeAI

llm = GoogleGenerativeAI(model="gemini-2.5-pro")

prompt = """
You are a helpful AI assistant that clean rooms. The room has three main elements:

1. Clothes: These can be either on the floor, in your hand, or in the hamper.
2. Books: These can be either scattered, in your hand, or on the shelf.
3. Wastebin: This can be either full or empty.

Your goal is to:
- Move clothes from the floor to the hamper.
- Place books from any location to the shelf
- Empty the wastebin if it is full

You have the following tools at your disposal: {tool_names}
Description of the tools: {tools}

To use a tool, respond exactly in this format:
   Thought: [Your reasoning about that action to take next]
   Action: [The name of the tool to use next]
   Action Input: [The dictionary representing the current room state]
   Observation: [Observe whether the room is tidy after the action is made]
   
Example:
    Thought: The clothes are on the floor. I should pick them up.
    Action: pick_up_clothes
    Action Input: {{"clothes": "floor", "books": "scattered", "wastebin": "full"}}
    Observation : The room is not yet tidy. Continue working
    
If the room is tidy, respond:
    Thought: The room is tidy, I should stop cleaning.
    Final Answer: The room is tidy. Final state achieved.
    
{agent_scratchpad}
"""


from langchain.prompts import PromptTemplate
from langchain.agents import create_react_agent
from langchain.agents import AgentExecutor


prompt_template = PromptTemplate(
    input_variable=["input", "tool_names", "tools", "agent_scratchpad"],
    template=prompt
)

agent = create_react_agent(llm=llm, tools=tools, prompt=prompt_template)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_steps=10,
                               handle_parsing_errors=True)

response = agent_executor.invoke(
    {
        'input': json.dumps(room_state),
        'tool_names': [tool.name for tool in tools],
        'tools': [tool.description for tool in tools]
    }
)

print()
print(response)        