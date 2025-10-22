import os

from langchain_openai import OpenAI, ChatOpenAI
from langgraph.constants import END
from langgraph.graph import StateGraph

from typing import List, TypedDict
from langchain_core.messages import HumanMessage, AIMessage

from dotenv import load_dotenv


class AgentState(TypedDict):
    messages : List[HumanMessage]
    ai_messages: List[AIMessage]

load_dotenv()
api_key = os.getenv('OPEN_AI_KEY')
llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)

def chat(state : AgentState) -> AgentState:
    human_message = input('User: ')
    state['messages'].append(HumanMessage(human_message))
    response = llm.invoke(human_message)
    state['ai_messages'].append(AIMessage(response.content))
    print(f'AI : {response.content}')
    return state

def should_continue(state : AgentState) -> str:
    if state['messages'][-1].content != 'exit':
        return 'loop'
    else:
        return 'exit'

graph = StateGraph(AgentState)
graph.add_node('process', chat)
graph.add_conditional_edges(
    'process',
    should_continue,
    {
        'loop' : 'process', #loop
        'exit' : END
    }
)
graph.set_entry_point('process')
graph.set_finish_point('process')
app = graph.compile()
app.invoke(AgentState(messages=[], ai_messages=[]))