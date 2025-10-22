from langgraph.graph import StateGraph, START, END
from conditionalgraph.agent_state import AgentState

def adder(state : AgentState) -> AgentState:
    """ This functions adds two numbers"""
    state['final'] = state['number1'] + state['number2']
    return state

def subtractor(state : AgentState) -> AgentState:
    """ This functions subtracts two numbers"""
    state['final'] = state['number1'] - state['number2']
    return state

def decide_next_node(state : AgentState) -> str:
    """ This functions routes to either adder or subtractor based on the operator"""
    if state['operator'] == '+':
        return "addition_operation"
    elif state['operator'] == '-':
        return "subtraction_operation"
    else:
        raise ValueError("Invalid operator")

graph = StateGraph(AgentState)

graph.add_node("router", lambda state: state)
graph.add_node("adder", adder)
graph.add_node("subtractor", subtractor)

graph.add_edge(START, "router")
graph.add_conditional_edges(
    "router",
    decide_next_node,
    {
        # Edge : Node
        "addition_operation": "adder",
        "subtraction_operation": "subtractor"
    }
)
graph.add_edge("router", END)
app = graph.compile()
response = app.invoke(AgentState(number1=5, operator='*', number2=10))
print(response)