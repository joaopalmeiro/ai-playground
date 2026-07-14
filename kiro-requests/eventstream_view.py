import json

from botocore.eventstream import EventStreamBuffer
from mitmproxy import contentviews


class AmazonEventStream(contentviews.Contentview):
    def prettify(self, data: bytes, metadata: contentviews.Metadata) -> str:
        buf = EventStreamBuffer()
        buf.add_data(data)

        chunks: list[str] = []
        response_chunks: list[str] = []

        for event in buf:
            headers = ", ".join(f"{k}={v}" for k, v in event.headers.items())
            chunks.append(f"# {headers}")

            text = event.payload.decode("utf-8")
            chunks.append(text)

            if event.headers.get(":event-type") == "assistantResponseEvent":
                response_chunks.append(json.loads(text)["content"])

        return f"{''.join(response_chunks)}\n---\n{'\n'.join(chunks)}"

    def render_priority(self, data: bytes, metadata: contentviews.Metadata) -> float:
        return 2 if metadata.content_type == "application/vnd.amazon.eventstream" else 0


contentviews.add(AmazonEventStream())
