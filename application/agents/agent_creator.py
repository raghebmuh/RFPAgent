from application.agents.classic_agent import ClassicAgent
from application.agents.react_agent import ReActAgent

# Try to import RFP agents, but don't fail if they have issues
try:
    from application.agents.rfp_agent import RFPAgent
    rfp_available = True
except Exception as e:
    print(f"Warning: Could not load RFPAgent: {e}")
    rfp_available = False

try:
    from application.agents.simple_rfp_agent import SimpleRFPAgent
    simple_rfp_available = True
except Exception as e:
    print(f"Warning: Could not load SimpleRFPAgent: {e}")
    simple_rfp_available = False

try:
    from application.agents.working_rfp_agent import WorkingRFPAgent
    working_rfp_available = True
except Exception as e:
    print(f"Warning: Could not load WorkingRFPAgent: {e}")
    working_rfp_available = False


class AgentCreator:
    agents = {
        "classic": ClassicAgent,
        "react": ReActAgent,
    }

    # Add RFP agents if available (prioritize WorkingRFPAgent)
    if working_rfp_available:
        agents["rfp"] = WorkingRFPAgent
        agents["reactrfp"] = WorkingRFPAgent
        agents["workingrfp"] = WorkingRFPAgent
    elif rfp_available:
        agents["rfp"] = RFPAgent
        agents["reactrfp"] = RFPAgent
    elif simple_rfp_available:
        agents["rfp"] = SimpleRFPAgent
        agents["reactrfp"] = SimpleRFPAgent
        agents["simplerfp"] = SimpleRFPAgent
    else:
        # Fallback: Use ReActAgent for RFP if specific agents aren't available
        agents["rfp"] = ReActAgent
        agents["reactrfp"] = ReActAgent

    @classmethod
    def create_agent(cls, type, *args, **kwargs):
        agent_class = cls.agents.get(type.lower())
        if not agent_class:
            raise ValueError(f"No agent class found for type {type}")
        return agent_class(*args, **kwargs)
