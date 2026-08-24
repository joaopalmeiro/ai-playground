from pathlib import Path

from ag_ui.core import RunAgentInput, UserMessage

PROMPT = "What's the weather forecast for Gaia tomorrow?"
OUTPUT = Path("request.json")

THREAD_ID = "thread-1"
RUN_ID = "run-1"
MESSAGE_ID = "msg-1"


if __name__ == "__main__":
    request = RunAgentInput(
        thread_id=THREAD_ID,
        run_id=RUN_ID,
        state={},
        messages=[UserMessage(id=MESSAGE_ID, role="user", content=PROMPT)],
        tools=[],
        context=[],
        forwarded_props=None,
    )

    OUTPUT.write_text(request.model_dump_json(indent=2) + "\n")
