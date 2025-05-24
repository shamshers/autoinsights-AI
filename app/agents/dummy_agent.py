# app/agents/dummy_agent.py

from agent_base import AgentBase

class DummyAgent(AgentBase):
    """
    An example agent that appends a test key to the state.
    """
    def run(self, state):
        state['dummy'] = 'Hello from DummyAgent!'
        return state
