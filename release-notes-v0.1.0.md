# Codex Blender Bridge v0.1.0

Initial release.

## What It Does

- Opens a local-only bridge at `127.0.0.1:9877`.
- Lets trusted local tools inspect the current Blender scene.
- Lets trusted local tools execute Python code inside Blender.
- Provides a separate port from common Blender MCP setups using `9876`.

## Install

Download `codex_blender_bridge_addon.zip`, then install it in Blender:

`Edit > Preferences > Add-ons > Install from Disk`

After installing, enable `Codex Blender Bridge`.

## Security

This add-on can execute Python code inside Blender. Enable it only on a trusted machine and do not expose the bridge port to a network.
