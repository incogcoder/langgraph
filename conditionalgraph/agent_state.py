from typing import TypedDict

class AgentState(TypedDict):
    number1 : int
    operator : str
    number2 : int
    final : int