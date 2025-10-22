from langgraph.constants import END
from langgraph.graph import StateGraph

from looping.agent_state import AgentState

def decide_next_node(state: AgentState) -> str:
    guess = state.guesses[-1]

    if guess == state.answer and state.attempts < 7:
        print("You win!")
        return "exit"

    if state.attempts >= 7:
        print("You lose!")
        return "exit"

    if guess < state.answer:
        print("You guessed lower than expected! Guess higher.")
    else:
        print("You guessed higher than expected! Guess lower.")

    return "loop"


def guessNode(state: AgentState) -> AgentState:
    guess = int(input('Guess a number between 1 & 20 inclusive: '))
    state.guesses.append(guess)
    state.attempts += 1
    return state

graph = StateGraph(AgentState)

graph.add_node("guessNode", guessNode)
graph.add_conditional_edges(
    "guessNode",
    decide_next_node, #Loop
    {
        # Edge : Node
        "loop" : "guessNode",
        "exit" : END
    }
)
graph.set_entry_point("guessNode")

app = graph.compile()
res = app.invoke(AgentState(player_name='Himanshu', answer=12))
print(res)
