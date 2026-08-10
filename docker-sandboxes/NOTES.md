# Notes

- https://www.docker.com/products/docker-sandboxes/
  - https://docs.docker.com/ai/sandboxes/get-started/
  - https://docs.docker.com/ai/sandboxes/faq/
  - https://docs.docker.com/ai/sandboxes/agents/kiro/
    - https://docs.docker.com/ai/sandboxes/agents/kiro/#base-image
  - https://docs.docker.com/reference/cli/sbx/policy/allow/network/
  - https://docs.docker.com/reference/cli/sbx/policy/deny/network/
  - https://docs.docker.com/reference/cli/sbx/policy/reset/

## Commands

```bash
sbx policy allow network "**"
```

```bash
sbx policy deny network "**"
```

```bash
sbx policy check network "**"
```

```bash
sbx policy reset --force
```
