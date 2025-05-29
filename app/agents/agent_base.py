# agents/base_agent.py

class AgentBaseMeta(type):
    registry = []

    def __new__(cls, name, bases, attrs):
        new_cls = super(AgentBaseMeta, cls).__new__(cls, name, bases, attrs)
        if name != "AgentBase":  # Skip base class itself
            AgentBaseMeta.registry.append(new_cls)
        return new_cls

class AgentBase(metaclass=AgentBaseMeta):
    def run(self, state: dict) -> dict:
        raise NotImplementedError("Each agent must implement `run()`.")
