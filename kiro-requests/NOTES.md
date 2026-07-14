# Notes

- https://github.com/joaopalmeiro/template-python-uv-script
- https://github.com/joaopalmeiro/ai-playground
- https://docs.mitmproxy.org/stable/addons/overview/
- https://docs.mitmproxy.org/stable/concepts/certificates/
  - https://docs.mitmproxy.org/stable/concepts/certificates/#installing-the-mitmproxy-ca-certificate-manually
- https://github.com/cereblab/grok-build-exfil-repro
- https://kiro.dev/docs/privacy-and-security/firewalls/#proxy-configuration
- https://github.com/jcheng5/mitm-vnd-amazon-eventstream
- https://kiro.dev/docs/cli/reference/built-in-tools/
- https://docs.mitmproxy.org/stable/overview/installation/#installation-from-the-python-package-index-pypi
  - https://pypi.org/project/mitmproxy/
- https://docs.aws.amazon.com/botocore/latest/reference/eventstream.html
- https://github.com/boto/botocore
- https://docs.mitmproxy.org/stable/addons/contentviews/
- `/generateAssistantResponse` endpoint

## Snippets

- https://github.com/cereblab/grok-build-exfil-repro/blob/4217f340dd10384436105191809c1af1f58b08ee/addon/log_xai.py

```python
# mitmdump addon: log every request to xAI/Google hosts (method, host, path,
# response status, request byte size) and SAVE the raw request bodies so we can
# later reconstruct what left the machine. Run via: mitmdump -s addon/log_xai.py
import os, time

OUT = os.environ.get("XAI_CAPTURE_DIR", os.path.expanduser("~/grok-exfil-capture"))
BODIES = os.path.join(OUT, "bodies")
HOSTS = ("grok.com", "xai", "googleapis", "amazonaws", "mixpanel")
os.makedirs(BODIES, exist_ok=True)


def response(flow):
    host = flow.request.pretty_host
    if not any(k in host for k in HOSTS):
        return
    status = flow.response.status_code if flow.response else "NORESP"
    body = flow.request.raw_content or b""
    path = flow.request.path.split("?")[0]
    with open(os.path.join(OUT, "wire.log"), "a") as log:
        log.write(f"{int(time.time())} {flow.request.method} {host}{path[:70]} -> {status} req={len(body)}b\n")
    # Save bodies of storage/upload calls so verify.sh can find the git bundle.
    if body and ("/v1/storage" in path or "storage" in host):
        fn = f"{int(time.time()*1000)}_{flow.request.method}_{len(body)}.bin"
        with open(os.path.join(BODIES, fn), "wb") as f:
            f.write(body)
```

- https://github.com/cereblab/grok-build-exfil-repro/blob/4217f340dd10384436105191809c1af1f58b08ee/scripts/setup-proxy.sh

```bash
#!/usr/bin/env bash
# One-time: generate + trust mitmproxy's CA, then start the logging proxy.
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
export XAI_CAPTURE_DIR="${XAI_CAPTURE_DIR:-$HOME/grok-exfil-capture}"
mkdir -p "$XAI_CAPTURE_DIR"

command -v mitmdump >/dev/null || { echo "install mitmproxy first: brew install mitmproxy"; exit 1; }

# Generate the CA on first run.
[ -f "$HOME/.mitmproxy/mitmproxy-ca-cert.pem" ] || (mitmdump -q & sleep 3; kill %1 2>/dev/null || true)

echo ">>> Trust the mitmproxy CA so Grok's TLS routes through the proxy:"
case "$(uname)" in
  Darwin) security add-trusted-cert -r trustRoot -k "$HOME/Library/Keychains/login.keychain-db" \
            "$HOME/.mitmproxy/mitmproxy-ca-cert.pem" || true ;;
  Linux)  echo "  sudo cp ~/.mitmproxy/mitmproxy-ca-cert.pem /usr/local/share/ca-certificates/mitmproxy.crt && sudo update-ca-certificates" ;;
esac

echo ">>> Starting capture proxy on 127.0.0.1:8080 (Ctrl-C to stop). Capture dir: $XAI_CAPTURE_DIR"
exec mitmdump -q -p 8080 -s "$HERE/addon/log_xai.py"
```

- https://github.com/cereblab/grok-build-exfil-repro/blob/4217f340dd10384436105191809c1af1f58b08ee/scripts/run-capture.sh

```bash
#!/usr/bin/env bash
# Run Grok in the target repo, routed through the capture proxy, with a prompt
# that explicitly tells it NOT to open any files. Anything that leaves is on the
# wire regardless of what the model "reads".
set -euo pipefail
REPO="${1:?usage: run-capture.sh <repo-dir>}"
REPO="$(cd "$REPO" && pwd)"

export HTTPS_PROXY=http://127.0.0.1:8080
export HTTP_PROXY=http://127.0.0.1:8080
export ALL_PROXY=http://127.0.0.1:8080
export SSL_CERT_FILE="$HOME/.mitmproxy/mitmproxy-ca-cert.pem"

GROK="${GROK_BIN:-$HOME/.grok/bin/grok}"
[ -x "$GROK" ] || { echo "grok not found at $GROK (set GROK_BIN)"; exit 1; }

echo ">>> setup-proxy.sh must be running in another terminal."
echo ">>> Running Grok in $REPO with: 'Reply with exactly: OK. Do not read or open any files.'"
"$GROK" -p "Reply with exactly: OK. Do not read or open any files." --cwd "$REPO"
echo ">>> done. Now run: ./scripts/verify.sh"
```
