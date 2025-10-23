import os
from langchain_openai import ChatOpenAI
from langgraph.constants import END
from langgraph.graph import StateGraph
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import HumanMessage, BaseMessage, SystemMessage
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

load_dotenv()
api_key = os.getenv('OPEN_AI_KEY')
llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)

conversation_history = []  # in-memory storage for chat history

# ---------------- Nodes ----------------

def init(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content=input('System Prompt: '))
    state['messages'] = [system_prompt]
    return state

def input_node(state: AgentState) -> AgentState:
    human_message = input('User: ')
    conversation_history.append('You: ' + human_message)
    state['messages'] = [HumanMessage(content=human_message)]
    return state

def model_call(state: AgentState) -> AgentState:
    response = llm.invoke(state['messages'])
    state['messages'] = [response]
    conversation_history.append('AI: ' + response.content)
    print(f'AI: {response.content}')
    return state

def save_chat(state: AgentState) -> AgentState:
    with open("log.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(conversation_history))
    print('========== Chat saved. ==========')
    return state

# ---------------- Conditional ----------------

def should_continue(state: AgentState):
    if state['messages'][-1].content.lower() == 'exit':
        return 'exit'
    else:
        return 'loop'

# ---------------- Graph ----------------

graph = StateGraph(AgentState)

graph.add_node('init', init)
graph.add_node('input_node', input_node)
graph.add_node('model_call', model_call)
graph.add_node('save_chat', save_chat)

graph.add_edge('init', 'input_node')

# Conditional edge from input_node
graph.add_conditional_edges(
    'input_node',
    should_continue,
    {
        'loop': 'model_call',  # call LLM if not exit
        'exit': 'save_chat'    # skip LLM if exit
    }
)


graph.add_edge('model_call', 'input_node')

graph.add_edge('save_chat', END)

graph.set_entry_point('init')
app = graph.compile()
app.invoke(AgentState(messages=[]))
