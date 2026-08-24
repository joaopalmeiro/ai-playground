from pydantic_ai import Agent
from pydantic_ai.mcp import MCPToolset
from pydantic_ai.models.test import TestModel

ipma = MCPToolset("http://localhost:3001/mcp")

agent = Agent(TestModel(), toolsets=[ipma])
