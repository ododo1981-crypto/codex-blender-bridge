# Security Policy

This project is unofficial and is not affiliated with OpenAI or Blender Foundation.

## Important Warning

Codex Blender Bridge can execute Python code inside Blender.

Only enable this add-on on a machine you trust. Only connect trusted local clients. Do not expose the bridge port to your network or the internet.

## Default Network Behavior

The add-on binds to:

```text
127.0.0.1
```

This means it accepts local connections from the same machine only.

Do not change the host binding to `0.0.0.0` unless you fully understand the risk.

## Reporting Security Issues

If you publish this project on GitHub, replace this section with your preferred contact method.

Suggested text:

```text
Please do not open a public issue for security reports.
Contact me by DM or email instead.
```

## Safe Use Checklist

- Keep the bridge bound to `127.0.0.1`.
- Do not run untrusted Python code.
- Disable the add-on when you do not need local automation.
- Avoid using it on shared or untrusted computers.
- Avoid running multiple automation tools against the same Blender file at the same time.
