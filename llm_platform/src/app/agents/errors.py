class AgentRegistryError(Exception):
    pass


class AgentAlreadyExistsError(AgentRegistryError):
    pass


class AgentNotFoundError(AgentRegistryError):
    pass


class AgentNotActiveError(AgentRegistryError):
    pass
