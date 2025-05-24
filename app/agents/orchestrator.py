# app/agents/orchestrator.py

from typing import List, Dict
from app.agents.agent_base import AgentBase

class OrchestratorAgent(AgentBase):
    """
    Orchestrator that runs a sequence of agents as a pipeline.
    """

    def __init__(self, agents: List[AgentBase]):
        self.agents = agents

    def run(self, state: Dict) -> Dict:
        for agent in self.agents:
            try:
                state = agent.run(state)
            except Exception as e:
                print(f"Error in {agent.__class__.__name__}: {e}")   # Add this line
                state['error'] = f"{agent.__class__.__name__} failed: {str(e)}"
                break
        return state
