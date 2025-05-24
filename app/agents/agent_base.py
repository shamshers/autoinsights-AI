# app/agents/agent_base.py

from abc import ABC, abstractmethod
from typing import Dict

class AgentBase(ABC):
    """
    Abstract base class for all agents.
    Each agent processes and returns a 'state' dictionary.
    """

    @abstractmethod
    def run(self, state: Dict) -> Dict:
        """
        Process input state and return updated state.
        """
        pass
