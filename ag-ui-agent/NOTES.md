# Notes

- https://github.com/joaopalmeiro/template-python-uv-script
- https://github.com/tambo-ai/tambo
- https://docs.ag-ui.com/concepts/architecture#message-types
- https://pydantic.dev/docs/ai/api/models/test/
- https://pydantic.dev/docs/ai/integrations/ui/overview/
  - "f you're building a chat app or other interactive frontend for an AI agent, your backend will need to receive agent run input (like a chat message or complete message history) from the frontend, and will need to stream the agent's events (like text, thinking, and tool calls) to the frontend so that the user knows what's happening in real time."
  - "(...) you'll typically want to use a UI event stream protocol that's natively supported by your frontend framework."
  - https://pydantic.dev/docs/ai/integrations/ui/ag-ui/
- https://github.com/pydantic/pydantic-ai/tree/6270fb37c1faf51213c4023c00594c95e963eaf8/examples/pydantic_ai_examples/ag_ui
- https://github.com/CopilotKit/CopilotKit/blob/4c975dad4983a78dc3a34418afe8fd34931480b8/skills/copilotkit-integrations/references/integrations/pydantic-ai.md?plain=1: "`AGUIAdapter.dispatch_request()` runs one AG-UI request and streams the protocol events back as SSE. Never share a single `StateDeps` instance across requests."
- https://pydantic.dev/docs/ai/overview/install/#slim-install
