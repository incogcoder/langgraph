from dataclasses import dataclass, field
from typing import List

@dataclass
class AgentState:
    player_name: str
    guesses: List[int] = field(default_factory=list)
    attempts: int = 0
    lower_bound: int = 1
    upper_bound: int = 20
    answer : int = 0
